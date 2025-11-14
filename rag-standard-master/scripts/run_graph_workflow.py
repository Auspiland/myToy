# scripts/run_graph_workflow.py
import sys
import os
import importlib
import argparse # 커맨드 라인 인자(예: 설정 파일 지정) 처리를 위함

# --- 프로젝트 루트 경로를 Python 경로에 추가 ---
# 이 스크립트(run_graph_workflow.py)가 'scripts' 폴더에 있다고 가정합니다.
# 프로젝트 루트는 'scripts' 폴더의 부모 디렉토리입니다.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# --- 유틸리티 임포트 ---
# config_setting.py에서 환경 변수 및 YAML 설정 로드 함수를 가져옵니다.
from rag_standard.utils.config_setting import load_env, load_yaml_config
# opensearch_manager.py에서 OpenSearch 관리 클래스를 가져옵니다.
from rag_standard.utils.opensearch_manager import OpenSearchManager
# KiwiTokenizer 임포트는 필요시 initialize_tokenizer_from_config 함수 내에서 처리됩니다.

# --- .env 파일 로드 (API 키, OpenSearch 인증 정보 등) ---
print("--- 환경 변수 로드 시작 ---")
load_env() # .env 파일에서 환경 변수를 로드합니다.
print("--- 환경 변수 로드 완료 ---")

# --- 전역 OpenSearch 접속 정보 (스크립트 시작 시 .env에서 로드) ---
# 이 변수들은 initialize_opensearch_manager_with_globals 함수에서 사용됩니다.
opensearch_host_global = os.getenv('OPENSEARCH_HOST')
opensearch_port_global = os.getenv('OPENSEARCH_PORT')
opensearch_user_global = os.getenv('OPENSEARCH_USER') # OpenSearch 사용자 이름
opensearch_password_global = os.getenv('OPENSEARCH_PASSWORD') # OpenSearch 비밀번호

def load_pipeline_config_from_util(config_path: str) -> dict:
    """
    파이프라인의 YAML 설정 파일을 rag_standard.utils.config_setting.load_yaml_config를 사용하여 로드합니다.

    Args:
        config_path (str): YAML 설정 파일의 경로입니다. 
                           절대 경로이거나 프로젝트 루트 기준의 상대 경로일 수 있습니다.

    Returns:
        dict: 로드된 설정 내용입니다.

    Raises:
        FileNotFoundError: 설정 파일을 찾을 수 없는 경우 발생합니다.
    """
    print("\n--- 파이프라인 설정 로드 시작 (config_setting.py 사용) ---")
    try:
        # config_setting.py의 load_yaml_config 함수는 내부적으로 경로를 처리합니다.
        config = load_yaml_config(config_path)
        # load_yaml_config 함수 내부에서 이미 "로드된 YAML config 경로"를 출력합니다.
        print(f"프로젝트명: {config.get('project_name', '이름 없는 프로젝트')}")
        print("--- 파이프라인 설정 로드 완료 ---")
        return config
    except FileNotFoundError as e:
        print(f"오류: 파이프라인 설정 파일을 로드할 수 없습니다. 경로: {config_path}, 오류: {e}")
        print("--- 파이프라인 설정 로드 실패 ---")
        raise
    except Exception as e:
        print(f"오류: 파이프라인 설정 로드 중 예상치 못한 문제 발생. 경로: {config_path}, 오류: {e}")
        print("--- 파이프라인 설정 로드 실패 ---")
        raise

def get_graph_runnable_from_config(config: dict):
    """
    설정 파일에 명시된 그래프 빌더 함수를 동적으로 로드하고 호출하여
    컴파일된 LangGraph 실행 가능 객체(runnable)를 가져옵니다.

    Args:
        config (dict): 파이프라인 설정입니다. 'graph_settings' 키를 포함해야 합니다.

    Returns:
        Any: 컴파일된 LangGraph 실행 가능 객체입니다.

    Raises:
        ValueError: 'graph_settings' 또는 필요한 하위 키가 설정에 없는 경우 발생합니다.
        ImportError: 그래프 모듈을 임포트할 수 없는 경우 발생합니다.
        AttributeError: 그래프 빌더 함수를 모듈에서 찾을 수 없는 경우 발생합니다.
        Exception: 그래프 빌드 중 기타 예외 발생 시 이를 다시 발생시킵니다.
    """
    print("\n--- 그래프 빌드 시작 ---")
    graph_cfg = config.get('graph_settings')
    if not graph_cfg:
        print("오류: 'graph_settings'를 파이프라인 설정에서 찾을 수 없습니다.")
        print("--- 그래프 빌드 실패 ---")
        raise ValueError("'graph_settings'를 파이프라인 설정에서 찾을 수 없습니다.")

    module_name = graph_cfg.get('module')
    builder_func_name = graph_cfg.get('builder_function')
    builder_args = graph_cfg.get('builder_args', {}) # 그래프 빌더 함수에 전달될 인자들

    if not module_name or not builder_func_name:
        print("오류: graph_settings에 그래프 'module' 또는 'builder_function'이 명시되지 않았습니다.")
        print("--- 그래프 빌드 실패 ---")
        raise ValueError("graph_settings에 그래프 'module' 또는 'builder_function'이 명시되지 않았습니다.")

    try:
        print(f"그래프 빌더 로드 시도: {module_name}.{builder_func_name}")
        module = importlib.import_module(module_name)
        builder_function = getattr(module, builder_func_name)
        runnable_graph = builder_function(**builder_args) # 빌더 함수에 인자 전달
        print(f"그래프 빌드 및 컴파일 성공: {module_name}.{builder_func_name}")
        print("--- 그래프 빌드 완료 ---")
        return runnable_graph
    except ImportError as e:
        print(f"오류: 그래프 모듈 '{module_name}'을 임포트할 수 없습니다: {e}")
        print("--- 그래프 빌드 실패 ---")
        raise
    except AttributeError as e:
        print(f"오류: 그래프 빌더 함수 '{builder_func_name}'를 모듈 '{module_name}'에서 찾을 수 없습니다: {e}")
        print("--- 그래프 빌드 실패 ---")
        raise
    except Exception as e:
        print(f"오류: {module_name}.{builder_func_name}을(를) 통한 그래프 빌드 중 예외 발생: {e}")
        print("--- 그래프 빌드 실패 ---")
        raise

def initialize_tokenizer_from_config(config: dict):
    """
    설정 파일의 'tokenizer' 섹션을 기반으로 토크나이저를 초기화합니다.

    Args:
        config (dict): 파이프라인 설정입니다. 'tokenizer' 키를 포함할 수 있습니다.

    Returns:
        object | None: 초기화된 토크나이저 객체 또는 설정이 없거나 실패 시 None을 반환합니다.
    """
    print("\n--- 토크나이저 초기화 시작 ---")
    tokenizer_config = config.get('tokenizer')
    if not tokenizer_config:
        print("토크나이저 설정이 YAML에 없습니다. 초기화를 건너뜁니다.")
        print("--- 토크나이저 초기화 완료 (건너뜀) ---")
        return None

    tokenizer_type = tokenizer_config.get('type', 'KiwiTokenizer') # 기본값으로 KiwiTokenizer 사용
    print(f"토크나이저 유형: {tokenizer_type}")

    if tokenizer_type == "KiwiTokenizer":
        try:
            # KiwiTokenizer의 실제 위치에 따라 임포트 경로를 확인해야 합니다.
            from rag_standard.utils.sparse_tokenizer import KiwiTokenizer
            
            included_pos_tags = tuple(tokenizer_config.get('included_pos_tags', ('NNG', 'NNP')))
            print(f"  포함될 품사 태그: {included_pos_tags}")
            
            dictionary_path_rel = tokenizer_config.get('dictionary_path')
            dictionary_path_abs = None
            if dictionary_path_rel: 
                dictionary_path_abs = os.path.join(PROJECT_ROOT, dictionary_path_rel)
                print(f"  사용자 사전 경로 (상대): {dictionary_path_rel} -> (절대): {dictionary_path_abs}")
                if not os.path.exists(dictionary_path_abs):
                    print(f"  경고: 토크나이저 사용자 사전 경로를 찾을 수 없습니다: {dictionary_path_abs}")
                    dictionary_path_abs = None # 경로가 없으면 None으로 설정하여 전달하지 않음
            else:
                print("  사용자 사전 경로가 설정되지 않았습니다.")

            tokenizer_init_args = {'included_pos_tags': included_pos_tags}
            if dictionary_path_abs:
                # KiwiTokenizer가 dictionary_path 인자를 지원한다고 가정합니다.
                tokenizer_init_args['dictionary_path'] = dictionary_path_abs
            
            tokenizer = KiwiTokenizer(**tokenizer_init_args)
            
            if dictionary_path_abs:
                 print(f"  KiwiTokenizer에 사용자 사전 경로 전달 시도됨: {dictionary_path_abs}")
            
            print(f"{tokenizer_type} 초기화 성공.")
            print("--- 토크나이저 초기화 완료 ---")
            return tokenizer
        except ImportError:
            print(f"  오류: {tokenizer_type} 클래스를 rag_standard.utils.sparse_tokenizer 에서 찾을 수 없습니다. 임포트 경로를 확인하세요.")
            print("--- 토크나이저 초기화 실패 ---")
            return None
        except Exception as e:
            print(f"  오류: {tokenizer_type} 초기화 중 예외 발생: {e}")
            print("--- 토크나이저 초기화 실패 ---")
            return None
    else:
        print(f"지원하지 않는 토크나이저 유형입니다: {tokenizer_type}")
        print("--- 토크나이저 초기화 실패 ---")
        return None

def initialize_opensearch_manager_with_globals() -> OpenSearchManager: # 반환 타입 변경
    """
    전역 변수(OPENSEARCH_HOST, PORT, USER, PASSWORD)를 사용하여 OpenSearchManager 인스턴스를 초기화합니다.
    rag_standard.utils.opensearch_manager.OpenSearchManager를 사용합니다.

    Returns:
        OpenSearchManager: OpenSearchManager 인스턴스입니다.

    Raises:
        ValueError: OpenSearch 호스트 또는 포트 정보가 환경 변수에 없는 경우 발생합니다.
        Exception: OpenSearchManager 초기화 또는 연결 중 오류 발생 시 이를 다시 발생시킵니다.
    """
    print("\n--- OpenSearch Manager 초기화 시작 ---") # 이름 변경: 클라이언트 -> Manager
    if not opensearch_host_global or not opensearch_port_global:
        print("오류: OPENSEARCH_HOST 또는 OPENSEARCH_PORT 환경 변수가 설정되지 않았습니다.")
        print("--- OpenSearch Manager 초기화 실패 ---")
        raise ValueError("OpenSearch 호스트 또는 포트 정보가 환경 변수에 없습니다.")
    
    opensearch_auth = None
    if opensearch_user_global and opensearch_password_global:
        opensearch_auth = (opensearch_user_global, opensearch_password_global)
        print(f"OpenSearch 연결 정보: 호스트='{opensearch_host_global}', 포트='{opensearch_port_global}', 인증 사용")
    else:
        print(f"OpenSearch 연결 정보: 호스트='{opensearch_host_global}', 포트='{opensearch_port_global}', 인증 미사용")
    
    try:
        # OpenSearchManager 인스턴스 생성
        manager = OpenSearchManager(
            host=opensearch_host_global,
            port=opensearch_port_global,
            http_auth=opensearch_auth
        )
        # OpenSearchManager._connect() 내부에서 연결 성공/실패 로그를 이미 출력합니다.
        print("--- OpenSearch Manager 초기화 완료 ---")
        return manager # OpenSearchManager 인스턴스 자체를 반환
    except Exception as e:
        # OpenSearchManager에서 발생한 예외(ValueError, ConnectionError 등)를 포함할 수 있습니다.
        print(f"오류: OpenSearch Manager 초기화 중 예외 발생: {e}")
        print("--- OpenSearch Manager 초기화 실패 ---")
        raise

def execute_rag_pipeline(
    pipeline_config: dict, 
    user_query: str,
    opensearch_manager_instance: OpenSearchManager = None, # 파라미터 이름 및 타입 변경
    tokenizer_instance = None,
    runnable_graph_instance = None 
    ) -> dict:
    """
    주어진 설정과 사용자 질문으로 RAG 파이프라인을 실행하고 최종 상태를 반환합니다.
    OpenSearch Manager, 토크나이저, 그래프를 외부에서 주입받아 재사용할 수 있습니다.

    Args:
        pipeline_config (dict): 파이프라인 설정입니다.
        user_query (str): 사용자의 질문입니다.
        opensearch_manager_instance (OpenSearchManager, optional): 미리 초기화된 OpenSearchManager 인스턴스입니다.
        tokenizer_instance (object, optional): 미리 초기화된 토크나이저입니다.
        runnable_graph_instance (Any, optional): 미리 빌드된 LangGraph 실행 가능 객체입니다.

    Returns:
        dict: 파이프라인 실행 후의 최종 상태(state)입니다. 오류 발생 시 'error' 키를 포함할 수 있습니다.
    """
    print(f"\n--- RAG 파이프라인 실행 시작 (질문: '{user_query}') ---")

    # 1. 토크나이저 결정 (주입 또는 신규 초기화)
    current_tokenizer = tokenizer_instance
    if not current_tokenizer:
        current_tokenizer = initialize_tokenizer_from_config(pipeline_config)
    else:
        print("기존 토크나이저 인스턴스를 사용합니다.")
        
    # 2. OpenSearch Manager 결정 (주입 또는 신규 초기화)
    current_opensearch_manager = opensearch_manager_instance # 변수 이름 변경
    if not current_opensearch_manager:
        current_opensearch_manager = initialize_opensearch_manager_with_globals() # 변수 이름 변경
    else:
        print("기존 OpenSearch Manager 인스턴스를 사용합니다.") # 메시지 변경
    
    ## 하이브리드 검색일 경우) YAML에 정의된 검색 파이프라인 생성/업데이트 시도
    vector_db_search_config = pipeline_config.get('graph_node_config', {}).get('vector_db_search', {})
    if vector_db_search_config.get('search_type') == 'hybrid':
        hybrid_search_config = vector_db_search_config.get('hybrid_search_config', {})

        if hybrid_search_config:
            normalization = hybrid_search_config['normalization']
            combination = hybrid_search_config['combination']
            weights = hybrid_search_config['weights']

            hybrid_search_pipeline_name = f"{normalization}_{combination}_{'_'.join([str(int(w*10)) for w in weights])}"

            print(f"\n--- '{hybrid_search_pipeline_name}' 검색 파이프라인 준비 중 (YAML 정의 사용) ---")
            
            if current_opensearch_manager.check_search_pipeline(hybrid_search_pipeline_name): # 파이프라인이 존재하면 그대로 사용
                print(f"--- '{hybrid_search_pipeline_name}' 검색 파이프라인이 존재하므로 생성하지 않습니다. ---")
            else: # 파이프라인이 존재하지 않으면 생성
                try:
                    current_opensearch_manager.create_search_pipeline(hybrid_search_pipeline_name, normalization, combination, weights)
                    # create_search_pipeline 내부에서 성공/실패 로그를 이미 출력합니다.
                    print(f"--- '{hybrid_search_pipeline_name}' 검색 파이프라인 준비 완료 ---")
                except Exception as e:
                    print(f"경고: '{hybrid_search_pipeline_name}' 검색 파이프라인 생성/업데이트 실패: {e}. 계속 진행합니다.")
                    # 파이프라인 생성 실패 시, 기존에 파이프라인이 존재하면 검색은 성공할 수 있음
                    # 또는 여기서 워크플로우를 중단하도록 선택할 수도 있습니다.
                    print(f"--- '{hybrid_search_pipeline_name}' 검색 파이프라인 준비 실패 ---")


    # 3. 실행 가능한 RAG 그래프 결정 (주입 또는 신규 빌드)
    current_runnable_graph = runnable_graph_instance
    if not current_runnable_graph:
        print("새로운 그래프 인스턴스를 빌드합니다...")
        try:
            current_runnable_graph = get_graph_runnable_from_config(pipeline_config)
        except Exception as e:
            return {
                "error": f"그래프 빌드 실패: {str(e)}", 
                "llm_answer": "오류로 인해 답변을 생성할 수 없습니다."
            }
    else:
        print("기존 그래프 인스턴스를 사용합니다.")

    # 4. 초기 상태 준비
    initial_state = {
        'user_query': user_query,
        'config': pipeline_config,
        'sparse_tokenizer': current_tokenizer, 
        'opensearch_manager': current_opensearch_manager, # 키 이름 변경: opensearch_client -> opensearch_manager
        'llm_stream_handled_by_node': False
    }
    print("파이프라인 초기 상태가 준비되었습니다.")

    # 5. 그래프 실행
    try:
        print("LangGraph 그래프 실행 중...")
        final_state = current_runnable_graph.invoke(initial_state)
        print("RAG 파이프라인 실행 성공.")
        print("--- RAG 파이프라인 실행 완료 ---")
        return final_state
    except Exception as e:
        print(f"RAG 파이프라인 실행 중 오류 발생: {e}")
        print("--- RAG 파이프라인 실행 실패 ---")
        return {
            "error": f"파이프라인 실행 오류: {str(e)}", 
            "llm_answer": f"파이프라인 실행 중 오류로 인해 답변을 생성할 수 없습니다: {e}"
        }

def display_pipeline_results(final_state: dict, pipeline_config: dict):
    """
    파이프라인 실행 결과를 콘솔에 보기 좋게 출력합니다.

    Args:
        final_state (dict): execute_rag_pipeline에서 반환된 최종 상태입니다.
        pipeline_config (dict): 파이프라인 설정입니다. (예: results_display_count)
    """
    print("\n\n================ 최종 결과 ================")
    print(f"사용자 질문: {final_state.get('user_query', '알 수 없음')}")
    
    if final_state.get("error"):
        print(f"오류 발생: {final_state['error']}")

    retrieved_docs = final_state.get('retrieved_documents')
    docs_to_display = pipeline_config.get('results_display_count', 3)

    if retrieved_docs:
        print(f"\n검색된 문서 ({len(retrieved_docs)}개 중 최대 {docs_to_display}개 표시):")
        for i, doc in enumerate(retrieved_docs[:docs_to_display]): 
             source = doc.get('_source', {})
             print(f"  문서 {i+1}: ID: {doc.get('_id', 'N/A')}, 점수: {doc.get('_score', 'N/A')}, 파일: {source.get('file_name', 'N/A')}")
    elif not final_state.get("error"): 
        print("\n검색된 문서가 없습니다.")

    if not final_state.get('llm_stream_handled_by_node', False):
        print(f"\nLLM 답변:\n{final_state.get('llm_answer', '생성된 답변이 없습니다.')}")
    else:
        print("\nLLM 답변: (스트리밍으로 이미 출력되었거나, 해당 노드에서 출력을 관리합니다)") 

    print("========================================")

def main_cli(config_file_path: str, query: str = ""):
    """
    커맨드 라인 인터페이스(CLI)를 위한 메인 RAG 파이프라인 실행 함수입니다.
    단일 질문을 처리하고 결과를 출력합니다.

    Args:
        config_file_path (str): 파이프라인 설정 YAML 파일 경로입니다.
        query (str, optional): 사용자의 질문입니다. 제공되지 않으면 설정 파일의 'example_query'를 사용합니다.
    """
    print("====== CLI RAG 워크플로우 (단일 질문) 시작 ======")
    try:
        pipeline_config = load_pipeline_config_from_util(config_file_path)
        user_query = query if query else pipeline_config.get("example_query", "기본 질문: 정보를 제공해주세요.")

        # OpenSearchManager 초기화
        opensearch_manager = initialize_opensearch_manager_with_globals()

        final_state = execute_rag_pipeline(
            pipeline_config, 
            user_query,
            opensearch_manager_instance=opensearch_manager # 초기화된 매니저 전달
            )
        display_pipeline_results(final_state, pipeline_config)
        
    except FileNotFoundError:
        print("설정 파일을 찾을 수 없어 워크플로우를 진행할 수 없습니다.")
    except ValueError as ve:
        print(f"입력값 또는 설정 오류로 워크플로우를 진행할 수 없습니다: {ve}")
    except Exception as e:
        print(f"CLI RAG 워크플로우 실행 중 예상치 못한 오류 발생: {e}")
        
    print("====== CLI RAG 워크플로우 (단일 질문) 종료 ======")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="설정 파일을 기반으로 RAG 워크플로우를 실행합니다.")
    parser.add_argument(
        "config_file", 
        type=str, 
        help="파이프라인 설정 YAML 파일 경로입니다. 프로젝트 루트를 기준으로 한 상대 경로 또는 절대 경로를 사용할 수 있습니다."
    )
    parser.add_argument(
        "-q", "--query",
        type=str,
        default=None, 
        help="파이프라인에 전달할 사용자 질문입니다. 지정하지 않으면 설정 파일의 'example_query'를 사용합니다."
    )
    args = parser.parse_args()
    
    if not opensearch_host_global or not opensearch_port_global:
        print("치명적 오류: OPENSEARCH_HOST 또는 OPENSEARCH_PORT 환경 변수가 설정되지 않았습니다. .env 파일을 확인하고 설정해주세요.")
        sys.exit(1)
    
    main_cli(args.config_file, args.query)