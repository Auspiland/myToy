from __future__ import annotations
from typing import List, Optional, Any, Dict
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field

from opensearchpy import OpenSearch
from opensearchpy.exceptions import TransportError


from rag_standard.utils import opensearch_manager
from rag_standard.utils.config_setting import load_yaml_config, load_env
from rag_standard.utils.model_call import embed_text, generate_llm_response
from rag_standard.graph_workflow.state import NaiveRAGState

from rag_standard.utils.sparse_tokenizer import KiwiTokenizer

# 환경변수 설정
load_env()


class HybridRequest(BaseModel):
    user_query: str
    index: str = 't3q_vector_index_khnp_20250901'
    # sparse_field: str = Field("content", description="BM25 필드")
    # text_query: str = Field(..., description="BM25용 텍스트 쿼리")
    # vector_field: str = Field(..., description="knn_vector 필드명")
    # query_vector: List[float] = Field(..., description="질의 임베딩 벡터")
    # k: int = Field(50, ge=1, le=1000)
    # num_candidates: int = Field(1000, ge=1, le=100000)
    # size: int = Field(10, ge=1, le=1000)
    # excludes: List[str] = Field(default_factory=list)
    # search_pipeline: Optional[str] = None

pipeline_config = load_yaml_config(os.path.abspath('./configs/naive_rag_workflow.yaml'))

app = FastAPI(title="Async OpenSearch via FastAPI (threadpool)")


@app.on_event("startup")
def on_startup():
    # OpenSearch client
    app.state.os = opensearch_manager.OpenSearchManager(os.getenv("OPENSEARCH_HOST"),os.getenv("OPENSEARCH_PORT"))


@app.on_event("startup")
def on_startup_tokenizer():
    # 토크나이저 (Kiwi)
    app.state.tokenizer = KiwiTokenizer(included_pos_tags=pipeline_config['tokenizer']['included_pos_tags'])

# -----------------------------
# 엔드포인트
# -----------------------------

@app.post("/search/hybrid")
async def search_hybrid(req: HybridRequest):
    # BM25 + top-level kNN 결합 (OpenSearch가 스코어를 병합)

    
    # Hybrid Search 검색 옵션
    normalization = pipeline_config['graph_node_config']['vector_db_search']['hybrid_search_config']['normalization']
    combination = pipeline_config['graph_node_config']['vector_db_search']['hybrid_search_config']['combination']
    weights = pipeline_config['graph_node_config']['vector_db_search']['hybrid_search_config']['weights']

    pipeline_name = normalization + '_' + combination + '_'  + str(int(weights[0]*10)) + '_' + str(int(weights[1]*(10)))

    # 검색 파이프라인 생성 없을 경우 생성
    if app.state.os.check_search_pipeline(pipeline_name) == False:
        app.state.os.create_search_pipeline(pipeline_name,normalization,combination,weights)
        
    else:
        pass

    '''
    ===============================
    naive_rag_worflow.yaml sample
    ===============================
    
    {'project_name': 'Naive RAG 표준화 데모',
     'description': 'RAG 표준화 데모용',
     'graph_settings': {'module': 'rag_standard.graph_workflow.graph',
      'builder_function': 'build_naive_rag_graph'},
     'tokenizer': {'type': 'KiwiTokenizer',
      'included_pos_tags': ['NNG', 'NNP', 'VV', 'VA'],
      'dictionary_path': ''},
     'graph_node_config': {'vector_db_search': {'index_name': 't3q_vector_index_khnp_20250901',
       'dense_vector_field': 'text_dense',
       'sparse_vector_field': 'text_sparse_kiwi',
       'k': 10,
       'size': 5,
       'search_type': 'hybrid',
       'hybrid_search_config': {'normalization': 'min_max',
        'combination': 'arithmetic_mean',
        'weights': [0.3, 0.7]}},
      'generate_answer': {'system_prompt_template': '너는 한국수력원자력 회사의 AI 비서이다. 사용자의 질문에 대해 문서를 참고하여 친절하고 정확하게 답변해야 한다.',
       'user_prompt_template': '## 사용자 질문:\n{user_query}\n\n## 참고 문서:\n{documents}\n\n## 답변:\n',
       'temperature': 0.7,
       'stream_output': True}},
     'evaluation_settings': {'qa_dataset_path': 'data/QA/qa_dataset.parquet',
      'results_output_dir': 'benchmark',
      'eval_type': 'retrieval',
      'k_retrieval': 5}}
    
    '''

    # HybridSearch 실행
    response = app.state.os.execute_hybrid_search_with_pipeline(
        # 인덱스명
        index_name = req.index,
        # HybridSearch 파이프라인명
        pipeline_name = pipeline_name,
        # 임베딩 벡터
        query_vector=json.loads(embed_text([req.user_query]).content.decode())['dense_vecs'][0],
        # 임베딩 벡터 저장 필드
        dense_field=pipeline_config['graph_node_config']['vector_db_search']['dense_vector_field'],
        # k 깂
        k_dense=pipeline_config['graph_node_config']['vector_db_search']['k'], # 'k'는 dense 검색의 k로 사용
        # 토크 나이징
        tokenized_query=app.state.tokenizer.tokenize(req.user_query),
        # sparse 벡터 저장 필드
        sparse_field=pipeline_config['graph_node_config']['vector_db_search']['sparse_vector_field'],
        # 검색 사이즈
        size=pipeline_config['graph_node_config']['vector_db_search']['size'],
        # 검색 결과 제외 필드
        source_excludes=['text_dense']
        )
    

    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_test:app", host="0.0.0.0", port=8502)
