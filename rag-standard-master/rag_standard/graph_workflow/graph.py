from langgraph.graph import StateGraph, START, END
from rag_standard.graph_workflow.state import NaiveRAGState
from rag_standard.graph_workflow.node import vector_db_search, generate_answer

# 참고: utils.opensearch_client.init_opensearch_client 와 utils.config_setting.load_env 는
# 이 모듈을 직접 사용하는 대신, 실행 스크립트(예: run_graph_workflow.py)에서 관리됩니다.

def build_naive_rag_graph():
    """
    표준 Naive RAG 그래프를 생성하고 컴파일하는 함수입니다.
    이 함수는 설정 파일의 'graph_settings'에 따라 동적으로 호출될 수 있습니다.
    """
    graph = StateGraph(NaiveRAGState)

    # 그래프에 노드(Node) 추가
    graph.add_node('vector_db_search', vector_db_search) # 벡터 DB 검색 노드
    graph.add_node('generate_answer', generate_answer)   # 답변 생성 노드

    # 그래프에 엣지(Edge) 추가 (노드 간의 흐름 정의)
    graph.add_edge(START, 'vector_db_search')             # 시작점에서 vector_db_search 노드로 이동
    graph.add_edge('vector_db_search', 'generate_answer') # vector_db_search 노드에서 generate_answer 노드로 이동
    graph.add_edge('generate_answer', END)                # generate_answer 노드에서 종료점으로 이동

    # 그래프 컴파일
    compiled_graph = graph.compile()
    print("Naive RAG 그래프가 빌드 및 컴파일되었습니다.")
    return compiled_graph

# 만약 다른 종류의 그래프 빌더 함수가 있다면 여기에 추가합니다.
# 예: def build_advanced_rag_graph(custom_param1: str): ...