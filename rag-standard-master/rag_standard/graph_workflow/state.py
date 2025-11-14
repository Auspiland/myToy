from typing import TypedDict, List, Dict, Any, Optional
# from rag_standard.utils.sparse_tokenizer import SparseTokenizer
# from rag_standard.utils.opensearch_manager import OpenSearchManager

# Naive RAG State 정의
class NaiveRAGState(TypedDict):
  config: Dict # 파이프라인 설정
  user_query: str # 사용자 질문
  sparse_tokenizer: Any # SparseTokenizer
  opensearch_manager: Any # OpenSearchManager
  retrieved_documents: List[dict] # 검색 결과
  llm_answer: str # LLM 답변
  # 스트리밍이 노드 레벨에서 처리되었는지 여부를 나타내는 플래그 (선택 사항)
  # 이 필드는 generate_answer 노드에서 설정될 수 있습니다.
  llm_stream_handled_by_node: Optional[bool] 