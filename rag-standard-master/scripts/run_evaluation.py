import os
import sys
import argparse
import pandas as pd
from typing import List, Dict, Set, Any, Optional
import numpy as np
import shutil
# import yaml # Not explicitly used for saving, shutil.copy2 handles config copy

# --- 프로젝트 루트 경로를 Python 경로에 추가 ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# --- 스크립트 및 유틸리티 임포트 ---
from scripts.run_graph_workflow import (
    load_pipeline_config_from_util as load_pipeline_config, # 이름 변경된 함수를 기존 이름으로 임포트
    execute_rag_pipeline,
    initialize_tokenizer_from_config,
    get_graph_runnable_from_config,
    # initialize_opensearch_manager_with_globals # run_evaluation은 자체 초기화 로직 사용
)
# OpenSearchManager 직접 임포트
from rag_standard.utils.opensearch_manager import OpenSearchManager
# 환경변수 로더 임포트
from rag_standard.utils.config_setting import load_env
# 평가 지표 함수들 임포트
from rag_standard.utils.evaluation_metrics import (
    precision_at_k,
    recall_at_k,
    f1_at_k,
    calculate_rouge,
    calculate_bleu,
)

# --- 초기 설정 (애플리케이션 시작 시 한 번 수행) ---
print("--- 환경 변수 로드 시작 ---")
load_env() # .env 파일에서 환경 변수를 로드합니다.
print("--- 환경 변수 로드 완료 ---")


def load_qa_dataset(file_path: Optional[str]) -> List[Dict[str, Any]]:
    """QA 데이터셋을 Parquet 파일에서 로드하고 전처리합니다."""
    dataset_to_return: List[Dict[str, Any]] = []
    if not file_path:
        print("오류: QA 데이터셋 파일 경로가 제공되지 않았습니다. 설정 파일의 'evaluation_settings.qa_dataset_path'를 확인하세요.")
        return dataset_to_return

    actual_path = file_path if os.path.isabs(file_path) else os.path.join(PROJECT_ROOT, file_path)
    print(f"QA 데이터셋 (Parquet) 로드 중: {actual_path}")
    try:
        df = pd.read_parquet(actual_path)
        dataset_to_return = df.to_dict(orient='records')
        print(f"QA 데이터셋 로드 완료: {len(dataset_to_return)}개 항목.")
    except FileNotFoundError:
        print(f"오류: QA 데이터셋 파일을 찾을 수 없습니다: {actual_path}")
        return []
    except ImportError:
        print("오류: Parquet 파일을 읽기 위해 'pandas'와 'pyarrow' 또는 'fastparquet' 라이브러리가 필요합니다.")
        print("      'pip install pandas pyarrow' 또는 'pip install pandas fastparquet'로 설치해주세요.")
        return []
    except Exception as e:
        print(f"오류: QA 데이터셋 Parquet 로드 중 예기치 않은 오류 발생 ({actual_path}): {e}")
        return []

    processed_dataset: List[Dict[str, Any]] = []
    for i, item in enumerate(dataset_to_return):
        if not isinstance(item, dict):
            print(f"경고: QA 데이터셋 항목 {i}이 딕셔너리가 아닙니다. 건너뜁니다.")
            continue
        if "query" not in item or item.get("query") is None:
            print(f"경고: QA 데이터셋 항목 {i}에 'query' 키가 없거나 값이 비어있습니다. 건너뜁니다.")
            continue

        # ground_truth_retrieved_doc_ids를 set of strings로 변환
        gt_doc_ids_val = item.get("ground_truth_retrieved_doc_ids")
        current_gt_ids = set()
        if gt_doc_ids_val is not None:
            if isinstance(gt_doc_ids_val, (list, set, np.ndarray)):
                # np.ndarray의 경우 tolist()로 변환 후 처리
                id_list = list(gt_doc_ids_val) if not isinstance(gt_doc_ids_val, np.ndarray) else gt_doc_ids_val.tolist()
                current_gt_ids = set(str(doc_id) for doc_id in id_list if doc_id is not None and str(doc_id).strip() != "")
            else:
                print(f"경고: QA 데이터셋 항목 {i}의 'ground_truth_retrieved_doc_ids' ({type(gt_doc_ids_val)})가 리스트/세트/ndarray가 아닙니다. 빈 세트로 처리합니다.")
        item["ground_truth_retrieved_doc_ids"] = current_gt_ids

        # ground_truth_answers를 list of strings로 변환
        gt_answers_val = item.get("ground_truth_answers")
        current_gt_answers = []
        if gt_answers_val is not None:
            if isinstance(gt_answers_val, list):
                current_gt_answers = [str(ans) for ans in gt_answers_val if ans is not None]
            elif isinstance(gt_answers_val, (str, np.str_)): # numpy 문자열도 처리
                current_gt_answers = [str(gt_answers_val)]
            elif isinstance(gt_answers_val, np.ndarray):
                current_gt_answers = [str(ans) for ans in gt_answers_val.tolist() if ans is not None]
            else:
                print(f"경고: QA 데이터셋 항목 {i}의 'ground_truth_answers' ({type(gt_answers_val)})가 리스트나 문자열이 아닙니다. 빈 리스트로 처리합니다.")
        item["ground_truth_answers"] = current_gt_answers
        
        processed_dataset.append(item)
    print(f"QA 데이터셋 전처리 완료. 유효한 항목 수: {len(processed_dataset)}")
    return processed_dataset


def calculate_single_item_retrieval_metrics(
    retrieved_doc_ids: List[str], 
    gt_doc_ids: Set[str], 
    k_value: int
) -> Dict[str, float]:
    """단일 항목에 대한 검색 지표를 계산합니다."""
    p_at_k = precision_at_k(retrieved_doc_ids, gt_doc_ids, k_value)
    r_at_k = recall_at_k(retrieved_doc_ids, gt_doc_ids, k_value)
    f1 = f1_at_k(p_at_k, r_at_k) # F1은 P@k와 R@k로부터 계산
    return {"p_at_k": p_at_k, "r_at_k": r_at_k, "f1_at_k": f1}

def calculate_single_item_generation_metrics(
    generated_answer: str,
    gt_answers: List[str] 
) -> Dict[str, Any]:
    """단일 항목에 대한 생성 지표(ROUGE-F1, BLEU)를 계산합니다."""
    if not gt_answers or not generated_answer.strip(): # 정답 답변이 없거나 생성된 답변이 비어있으면 점수는 0
        return {
            "rouge1_f": 0.0, "rouge2_f": 0.0, "rougeL_f": 0.0,
            "bleu": 0.0
        }

    # calculate_rouge는 [(gen, [ref1, ref2]), ...] 형태를 기대하지 않고, [gen1, gen2], [[ref1a, ref1b], [ref2a, ref2b]] 형태를 기대합니다.
    # 단일 항목이므로: [generated_answer], [[gt_answer1, gt_answer2, ...]]
    rouge_scores_list = calculate_rouge(hypotheses=[generated_answer], references_list_of_lists=[gt_answers])
    rouge_scores_for_item = rouge_scores_list[0] if rouge_scores_list else {} # 첫 번째 (그리고 유일한) 항목의 점수
    
    # calculate_bleu는 [gen1, gen2], [[[ref1a], [ref1b]], [[ref2a], [ref2b]]] 형태를 기대.
    # 단일 항목이므로: [generated_answer], [[[gt_answer1, gt_answer2, ...]]]
    bleu_score = calculate_bleu(hypotheses=[generated_answer], references_list_of_lists_of_lists=[[gt_answers]])[0]


    return {
        "rouge1_f": rouge_scores_for_item.get('rouge1', {}).get('fmeasure', 0.0),
        "rouge2_f": rouge_scores_for_item.get('rouge2', {}).get('fmeasure', 0.0),
        "rougeL_f": rouge_scores_for_item.get('rougeL', {}).get('fmeasure', 0.0),
        "bleu": bleu_score
    }

def summarize_and_save_results(
        all_metrics_for_trial: List[Dict[str, Any]], 
        eval_type_flags: Dict[str, bool],
        output_dir_path: str,
        k_retrieval: Optional[int] = None
    ) -> Dict[str, Any]:
    """모든 평가 결과를 요약하고, 출력하며, 요약본을 CSV 파일로 저장합니다."""
    summary_data = {}
    if not all_metrics_for_trial:
        print("평가된 항목이 없어 요약을 생성할 수 없습니다.")
        summary_df = pd.DataFrame([summary_data]) # 빈 데이터라도 헤더는 있도록
        summary_file_path = os.path.join(output_dir_path, "summary_metrics.csv")
        try:
            summary_df.to_csv(summary_file_path, index=False, encoding='utf-8-sig')
            print(f"\n요약된 평가 지표 파일이 다음 위치에 생성되었습니다 (내용 없음): {summary_file_path}")
        except Exception as e:
            print(f"오류: 빈 요약 평가 지표 저장 중 오류 발생 ({summary_file_path}): {e}")
        return summary_data

    num_total_items_processed = len(all_metrics_for_trial)
    print(f"\n--- 전체 평가 요약 (총 {num_total_items_processed}개 항목 처리) ---")
    summary_data["total_items_processed"] = num_total_items_processed

    if eval_type_flags.get("retrieval"):
        # 'p_at_k'가 존재하는 항목만 검색 평가 대상으로 간주
        retrieval_scored_items = [item for item in all_metrics_for_trial if "p_at_k" in item]
        if retrieval_scored_items:
            num_retrieval_evaluated = len(retrieval_scored_items)
            avg_p_at_k = sum(m['p_at_k'] for m in retrieval_scored_items) / num_retrieval_evaluated
            avg_r_at_k = sum(m['r_at_k'] for m in retrieval_scored_items) / num_retrieval_evaluated
            avg_f1_at_k = sum(m['f1_at_k'] for m in retrieval_scored_items) / num_retrieval_evaluated
            
            print(f"\n  -- 검색 성능 (P/R/F1 @{k_retrieval}) --")
            print(f"  검색 평가된 질문 수: {num_retrieval_evaluated}")
            print(f"  평균 Precision@{k_retrieval}: {avg_p_at_k:.4f}")
            print(f"  평균 Recall@{k_retrieval}: {avg_r_at_k:.4f}")
            print(f"  평균 F1-score@{k_retrieval}: {avg_f1_at_k:.4f}")
            summary_data.update({
                f"retrieval_evaluated_queries_count_at_{k_retrieval}": num_retrieval_evaluated,
                f"avg_precision_at_{k_retrieval}": avg_p_at_k,
                f"avg_recall_at_{k_retrieval}": avg_r_at_k,
                f"avg_f1_at_{k_retrieval}": avg_f1_at_k,
            })
        else:
            print("\n  -- 검색 성능 --")
            print("  검색 평가를 수행할 유효한 항목이 없었습니다 (예: 'ground_truth_retrieved_doc_ids' 누락).")
            summary_data[f"retrieval_evaluated_queries_count_at_{k_retrieval}"] = 0

    if eval_type_flags.get("generation"):
        # 'rouge1_f'가 존재하는 항목만 생성 평가 대상으로 간주
        generation_scored_items = [item for item in all_metrics_for_trial if "rouge1_f" in item]
        if generation_scored_items:
            num_generation_evaluated = len(generation_scored_items)
            avg_rouge1_f = sum(m['rouge1_f'] for m in generation_scored_items) / num_generation_evaluated
            avg_rouge2_f = sum(m['rouge2_f'] for m in generation_scored_items) / num_generation_evaluated
            avg_rougeL_f = sum(m['rougeL_f'] for m in generation_scored_items) / num_generation_evaluated
            avg_bleu = sum(m['bleu'] for m in generation_scored_items) / num_generation_evaluated

            print(f"\n  -- 생성 성능 (ROUGE F1, BLEU) --")
            print(f"  생성 평가된 질문 수: {num_generation_evaluated}")
            print(f"  평균 ROUGE-1 F1: {avg_rouge1_f:.4f}")
            print(f"  평균 ROUGE-2 F1: {avg_rouge2_f:.4f}")
            print(f"  평균 ROUGE-L F1: {avg_rougeL_f:.4f}")
            print(f"  평균 BLEU: {avg_bleu:.4f}")
            summary_data.update({
                "generation_evaluated_queries_count": num_generation_evaluated,
                "avg_rouge1_f": avg_rouge1_f,
                "avg_rouge2_f": avg_rouge2_f,
                "avg_rougeL_f": avg_rougeL_f,
                "avg_bleu": avg_bleu,
            })
        else:
            print("\n  -- 생성 성능 --")
            print("  생성 평가를 수행할 유효한 항목이 없었습니다 (예: 'ground_truth_answers' 누락).")
            summary_data["generation_evaluated_queries_count"] = 0
    
    summary_df = pd.DataFrame([summary_data]) 
    summary_file_path = os.path.join(output_dir_path, "summary_metrics.csv")
    try:
        summary_df.to_csv(summary_file_path, index=False, encoding='utf-8-sig')
        print(f"\n요약된 평가 지표가 다음 파일에 저장되었습니다: {summary_file_path}")
    except Exception as e:
        print(f"오류: 요약된 평가 지표 저장 중 오류 발생 ({summary_file_path}): {e}")
    
    return summary_data

def get_next_trial_output_path(base_results_dir_from_config: str) -> str:
    """
    다음 평가 시도의 결과 저장 디렉토리 경로를 결정합니다 (예: base_path/0, base_path/1).
    base_results_dir_from_config는 YAML에 지정된 기본 결과 디렉토리입니다.
    """
    base_dir_abs = base_results_dir_from_config \
        if os.path.isabs(base_results_dir_from_config) \
        else os.path.join(PROJECT_ROOT, base_results_dir_from_config)

    os.makedirs(base_dir_abs, exist_ok=True)
    
    existing_trials = []
    for item_name in os.listdir(base_dir_abs):
        item_path = os.path.join(base_dir_abs, item_name)
        if os.path.isdir(item_path) and item_name.isdigit():
            existing_trials.append(int(item_name))
    
    next_trial_num = 0
    if existing_trials:
        next_trial_num = max(existing_trials) + 1
        
    new_trial_path = os.path.join(base_dir_abs, str(next_trial_num))
    return new_trial_path


def main():
    parser = argparse.ArgumentParser(description="RAG 파이프라인 평가 스크립트")
    parser.add_argument(
        "config_file",
        type=str,
        help="파이프라인 및 평가 설정 YAML 파일 경로 (프로젝트 루트 기준 상대 경로 또는 절대 경로)."
    )
    args = parser.parse_args()

    print("====== RAG 파이프라인 평가 시작 ======")
    
    pipeline_config_path = args.config_file if os.path.isabs(args.config_file) else os.path.join(PROJECT_ROOT, args.config_file)
    try:
        pipeline_config = load_pipeline_config(pipeline_config_path) # Alias된 함수 사용
    except FileNotFoundError:
        print(f"오류: 설정 파일을 찾을 수 없습니다 - {pipeline_config_path}")
        return
    except Exception as e:
        print(f"오류: 설정 파일 로드 중 예외 발생 ({pipeline_config_path}) - {e}")
        return

    eval_settings = pipeline_config.get('evaluation_settings')
    if not eval_settings or not isinstance(eval_settings, dict):
        print(f"오류: 설정 파일({pipeline_config_path})에 'evaluation_settings' 섹션이 없거나 올바르지 않습니다.")
        return

    eval_type_input = eval_settings.get('eval_type', 'all').lower()
    qa_dataset_path = eval_settings.get('qa_dataset_path')
    k_retrieval_default = 3 # 검색 평가 시 상위 K개
    k_retrieval = eval_settings.get('k_retrieval', k_retrieval_default)
    base_results_dir_from_config = eval_settings.get('results_output_dir', "results") # YAML에서 결과 저장 기본 디렉토리

    if not qa_dataset_path:
        print("오류: 설정 파일 'evaluation_settings'에 'qa_dataset_path'가 지정되지 않았습니다.")
        return
    if not isinstance(k_retrieval, int) or k_retrieval <= 0:
        print(f"경고: 설정 파일의 'k_retrieval' 값({k_retrieval})은 양의 정수여야 합니다. 기본값 {k_retrieval_default}을 사용합니다.")
        k_retrieval = k_retrieval_default

    try:
        output_dir_path = get_next_trial_output_path(base_results_dir_from_config)
        os.makedirs(output_dir_path, exist_ok=True)
        print(f"평가 결과는 다음 디렉토리에 저장됩니다: {output_dir_path}")
    except Exception as e:
        # output_dir_path가 정의되지 않았을 수 있으므로, base_results_dir_from_config를 대신 사용
        error_path_info = output_dir_path if 'output_dir_path' in locals() else base_results_dir_from_config
        print(f"오류: 결과 저장 디렉토리 생성 중 오류 발생 ({error_path_info}): {e}")
        return
        
    try:
        config_filename = os.path.basename(pipeline_config_path) 
        config_copy_path = os.path.join(output_dir_path, config_filename)
        shutil.copy2(pipeline_config_path, config_copy_path)
        print(f"설정 파일 복사본이 다음 위치에 저장되었습니다: {config_copy_path}")
    except Exception as e:
        print(f"경고: 설정 파일 복사 중 오류 발생: {e}")


    qa_dataset = load_qa_dataset(qa_dataset_path)
    if not qa_dataset:
        print("오류: QA 데이터셋을 로드할 수 없거나 유효한 항목이 없습니다. 평가를 종료합니다.")
        return

    # --- 공유 컴포넌트 초기화 (한 번) ---
    # OpenSearchManager 초기화
    shared_opensearch_manager = None
    try:
        opensearch_host = os.getenv('OPENSEARCH_HOST')
        opensearch_port_str = os.getenv('OPENSEARCH_PORT')
        opensearch_user = os.getenv('OPENSEARCH_USER')
        opensearch_password = os.getenv('OPENSEARCH_PASSWORD')

        if not opensearch_host or not opensearch_port_str:
            raise ValueError("OPENSEARCH_HOST 또는 OPENSEARCH_PORT 환경 변수가 설정되지 않았습니다.")
        
        opensearch_port = int(opensearch_port_str)
        opensearch_auth = (opensearch_user, opensearch_password) if opensearch_user and opensearch_password else None
        
        print(f"OpenSearch Manager 초기화 시도: 호스트='{opensearch_host}', 포트='{opensearch_port}', 인증={'사용' if opensearch_auth else '미사용'}")
        shared_opensearch_manager = OpenSearchManager(
            host=opensearch_host,
            port=opensearch_port,
            http_auth=opensearch_auth
        )
        # OpenSearchManager 생성자 내부에서 ping을 통해 연결 확인 및 로깅
        print("OpenSearch Manager 초기화 성공 (연결 확인은 Manager 내부에서 수행).")
    except ValueError as ve: # 포트 변환 오류 등
        print(f"오류: OpenSearch 설정값 오류 - {ve}")
        return
    except ConnectionError as ce: # OpenSearchManager 내부에서 연결 실패 시 발생 가능
        print(f"오류: OpenSearch 연결 실패 - {ce}")
        return
    except Exception as e: # 기타 예외
        print(f"오류: OpenSearch Manager 초기화 중 예외 발생 - {e}")
        return

    # 토크나이저 초기화
    shared_tokenizer = initialize_tokenizer_from_config(pipeline_config)
    # 필요시 토크나이저 초기화 실패에 대한 추가 처리
    if pipeline_config.get('tokenizer') and shared_tokenizer is None:
        print("경고: YAML에 토크나이저 설정이 있지만, 초기화에 실패했습니다. 일부 기능이 제한될 수 있습니다.")
    
    # 그래프 실행 객체 빌드
    shared_runnable_graph = None
    try:
        shared_runnable_graph = get_graph_runnable_from_config(pipeline_config)
        if shared_runnable_graph is None: # get_graph_runnable_from_config가 None을 반환할 수도 있다고 가정 (예외 대신)
             raise ValueError("그래프 실행 객체를 빌드하지 못했습니다 (None 반환).")
    except Exception as e:
        print(f"오류: 그래프 실행 객체 빌드 중 예외 발생 - {e}")
        return
    # --- 공유 컴포넌트 초기화 완료 ---

    all_results_for_trial: List[Dict[str, Any]] = []
    
    eval_type_flags = {
        "retrieval": eval_type_input == 'retrieval' or eval_type_input == 'all',
        "generation": eval_type_input == 'generation' or eval_type_input == 'all',
    }

    print(f"\n--- 전체 QA 데이터셋 ({len(qa_dataset)}개 항목) 처리 시작 ---")
    for i, qa_item in enumerate(qa_dataset):
        query = qa_item.get('query')
        # QA 항목별 고유 ID가 있다면 사용, 없다면 순번으로 생성
        query_id = qa_item.get('id', qa_item.get('query_id', f"item_{i+1}")) 

        if query is None: # query가 None인 경우 건너뛰기 (load_qa_dataset에서 이미 처리했어야 함)
            print(f"  항목 {query_id}: 'query'가 없어 건너뜁니다. (load_qa_dataset 확인 필요)")
            continue
        
        print(f"\n  항목 {i+1}/{len(qa_dataset)} (ID: {query_id}): {str(query)[:70]}...")

        final_state = execute_rag_pipeline(
            pipeline_config=pipeline_config,
            user_query=str(query), # 명시적으로 문자열로 변환
            opensearch_manager_instance=shared_opensearch_manager, # OpenSearchManager 인스턴스 전달
            tokenizer_instance=shared_tokenizer,
            runnable_graph_instance=shared_runnable_graph
        )

        # final_state에서 'llm_answer' 키를 사용 (run_graph_workflow.py의 execute_rag_pipeline 반환값 기준)
        llm_answer_output = str(final_state.get('llm_answer', "")) 
        retrieved_docs_output = final_state.get('retrieved_documents', [])

        current_item_metrics = {"query_id": query_id, "query": str(query)}

        if eval_type_flags["retrieval"]:
            gt_doc_ids: Set[str] = qa_item.get('ground_truth_retrieved_doc_ids', set())
            if gt_doc_ids: # 정답 문서 ID가 있는 경우에만 검색 평가 수행
                retrieved_doc_ids = [doc['_id'] for doc in retrieved_docs_output if isinstance(doc, dict) and '_id' in doc]
                retrieval_scores = calculate_single_item_retrieval_metrics(
                    retrieved_doc_ids, gt_doc_ids, k_retrieval
                )
                current_item_metrics.update(retrieval_scores)
                current_item_metrics["retrieved_doc_ids_eval"] = retrieved_doc_ids[:k_retrieval] # 평가에 사용된 상위 K개 ID 저장
                current_item_metrics["gt_doc_ids_eval"] = sorted(list(gt_doc_ids)) # 비교를 위해 정렬된 리스트로 저장
                print(f"    검색 P@{k_retrieval}: {retrieval_scores['p_at_k']:.4f}, R@{k_retrieval}: {retrieval_scores['r_at_k']:.4f}, F1@{k_retrieval}: {retrieval_scores['f1_at_k']:.4f}")
            else:
                print(f"    항목 {query_id}: 'ground_truth_retrieved_doc_ids'가 없어 검색 평가를 건너뜁니다.")
        
        if eval_type_flags["generation"]:
            gt_answers: List[str] = qa_item.get('ground_truth_answers', [])
            if gt_answers: # 정답 답변이 있는 경우에만 생성 평가 수행
                generation_scores = calculate_single_item_generation_metrics(
                    llm_answer_output, gt_answers
                )
                current_item_metrics.update(generation_scores)
                current_item_metrics["generated_answer_eval"] = llm_answer_output
                current_item_metrics["gt_answers_eval"] = gt_answers 
                print(f"    생성된 답변 (일부): {llm_answer_output[:50].replace(os.linesep, ' ')}...")
                print(f"    생성 ROUGE-L F1: {generation_scores['rougeL_f']:.4f}, BLEU: {generation_scores['bleu']:.4f}")
            else:
                print(f"    항목 {query_id}: 'ground_truth_answers'가 없어 생성 평가를 건너뜁니다.")
        
        # 유효한 메트릭이 하나라도 계산된 경우에만 결과에 추가 (query_id, query 외에)
        if len(current_item_metrics) > 2: 
            all_results_for_trial.append(current_item_metrics)
    
    print(f"\n--- 전체 QA 데이터셋 처리 완료 ---")

    if all_results_for_trial:
        detailed_results_df = pd.DataFrame(all_results_for_trial)
        detailed_results_file_path = os.path.join(output_dir_path, "detailed_evaluation_results.csv")
        try:
            detailed_results_df.to_csv(detailed_results_file_path, index=False, encoding='utf-8-sig')
            print(f"\n상세 평가 결과가 다음 파일에 저장되었습니다: {detailed_results_file_path}")
        except Exception as e:
            print(f"오류: 상세 평가 결과 저장 중 오류 발생 ({detailed_results_file_path}): {e}")

    summarize_and_save_results(all_results_for_trial, eval_type_flags, output_dir_path, k_retrieval)

    print("\n====== RAG 파이프라인 평가 종료 ======")

if __name__ == "__main__":
    main()