# scripts/cli_chat.py
import sys
import os
import argparse

# --- 프로젝트 루트 경로를 Python 경로에 추가 ---
# 이 스크립트가 scripts/ 내에 있으므로, 부모 디렉토리(프로젝트 루트)를 경로에 추가합니다.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# run_graph_workflow.py 에서 필요한 함수들을 가져옵니다.
# .env 로드 및 전역 변수(opensearch_host_global 등)는 run_graph_workflow 임포트 시 설정됩니다.
from scripts.run_graph_workflow import (
    load_pipeline_config_from_util as load_pipeline_config, # 이름 변경된 함수를 기존 이름으로 임포트
    initialize_tokenizer_from_config,
    initialize_opensearch_manager_with_globals, # 이름 변경된 함수 임포트
    get_graph_runnable_from_config,
    execute_rag_pipeline
)
# 환경 변수는 run_graph_workflow 모듈이 임포트될 때 이미 로드됩니다.

def start_chat_session(config_file_path: str):
    """효율적인 대화형 CLI 채팅 세션을 시작합니다."""
    print("\n====== 대화형 RAG CLI 채팅 (스트리밍 지원) 시작 ======")
    
    # 1. 파이프라인 설정 로드 (한 번)
    print("채팅 세션 초기화 중: 파이프라인 설정 로드...")
    pipeline_config = load_pipeline_config(config_file_path) #エイリアス된 load_pipeline_config 사용
    
    # 2. OpenSearch Manager 초기화 (한 번)
    print("채팅 세션 초기화 중: OpenSearch Manager 연결...")
    shared_opensearch_manager = initialize_opensearch_manager_with_globals() # 이름 변경된 함수 호출 및 변수명 변경
    
    # 3. 토크나이저 초기화 (한 번)
    print("채팅 세션 초기화 중: 토크나이저 로드...")
    shared_tokenizer = initialize_tokenizer_from_config(pipeline_config)
    
    # 4. 그래프 빌드 (한 번)
    print("채팅 세션 초기화 중: RAG 그래프 빌드...") 
    try:
        shared_runnable_graph = get_graph_runnable_from_config(pipeline_config) 
    except Exception as e:
        print(f"치명적 오류: 채팅 세션 시작을 위한 그래프 빌드에 실패했습니다: {e}")
        print("====== 대화형 RAG CLI 채팅 종료 ======")
        return
        
    print("\n--- 채팅 준비 완료 ---")
    print("종료하려면 'exit' 또는 'quit'을 입력하세요.")

    # 스트리밍 설정 여부는 최종 상태(final_state)의 'llm_stream_handled_by_node'로 판단하므로,
    # 여기서 pipeline_config에서 미리 읽어둘 필요는 필수는 아닙니다.
    # (참고) 스트리밍 설정 확인 (필요시):
    # stream_is_configured = pipeline_config.get('graph_node_config', {}).get('generate_answer', {}).get('stream_output', False)
    # print(f"(정보: 답변 스트리밍 설정 감지됨: {stream_is_configured})")

    while True:
        try:
            user_input = input("\n나: ") # 프롬프트 변경
            if user_input.lower() in ["exit", "quit", "종료", "나가기"]:
                print("챗봇: 채팅을 종료합니다. 이용해주셔서 감사합니다.")
                break
            if not user_input.strip():
                continue

            print("챗봇: ", end='', flush=True) # "답변: " -> "챗봇: "으로 변경, 스트리밍 시 바로 보임

            # 이미 초기화된 컴포넌트와 그래프를 전달하여 파이프라인 실행
            final_state = execute_rag_pipeline(
                pipeline_config=pipeline_config,
                user_query=user_input,
                opensearch_manager_instance=shared_opensearch_manager, # 수정된 파라미터명 사용
                tokenizer_instance=shared_tokenizer,
                runnable_graph_instance=shared_runnable_graph
            )
            
            # 노드에서 스트리밍을 처리한 경우 (llm_stream_handled_by_node=True),
            # generate_answer 노드가 print(..., end='') 및 마지막 print()로 출력을 완료했을 것입니다.
            # 따라서 여기서 llm_answer를 다시 출력하지 않습니다.
            if not final_state.get('llm_stream_handled_by_node', False): # 노드가 스트리밍을 처리하지 않은 경우
                if final_state.get("error"):
                    # 오류 메시지는 execute_rag_pipeline 또는 노드 내부에서 이미 상세히 출력되었을 수 있습니다.
                    # llm_answer에 오류 관련 내용이 담겨있을 수도 있습니다.
                    print(f"{final_state.get('llm_answer', '답변 생성 중 오류가 발생했습니다.')}") 
                else:
                    # 스트리밍을 하지 않았고, 오류도 없다면 llm_answer를 여기서 출력합니다.
                    print(f"{final_state.get('llm_answer', '답변을 생성하지 못했습니다.')}")
            # else: 노드가 스트리밍을 처리하고 줄바꿈까지 완료했다면, 여기서 추가적인 print()는 불필요합니다.

        except KeyboardInterrupt:
            print("\n챗봇: 사용자에 의해 채팅이 중단되었습니다. 종료합니다.")
            break
        except Exception as e:
            print(f"\n챗봇: 채팅 중 예상치 못한 오류가 발생했습니다: {e}")
            # 심각한 오류 시 세션 종료 또는 계속 진행 여부 결정 가능
            # 여기서는 계속 진행하도록 둡니다.
    
    print("====== 대화형 RAG CLI 채팅 종료 ======")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="설정 파일을 기반으로 RAG 채팅 세션을 시작합니다.")
    parser.add_argument(
        "config_file", 
        type=str, 
        help="파이프라인 설정 YAML 파일 경로입니다. 프로젝트 루트 기준 상대 경로 또는 절대 경로를 사용할 수 있습니다."
    )
    args = parser.parse_args()

    # run_graph_workflow 모듈 임포트 시 .env 파일이 로드되고 OPENSEARCH_HOST 등의 전역 변수가 설정됩니다.
    # 이 스크립트 실행 전에 해당 환경 변수가 유효한지 확인합니다.
    if not os.getenv('OPENSEARCH_HOST') or not os.getenv('OPENSEARCH_PORT'):
         print("치명적 오류: OPENSEARCH_HOST 또는 OPENSEARCH_PORT 환경 변수가 .env 파일에 설정되지 않았거나 유효하지 않습니다.")
         print("프로그램을 종료합니다.")
    else:
        start_chat_session(args.config_file)