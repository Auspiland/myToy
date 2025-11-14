# rag_standard/graph_workflow/node.py
from rag_standard.utils.model_call import embed_text, generate_llm_response
from rag_standard.graph_workflow.state import NaiveRAGState
# from rag_standard.utils.opensearch_manager import OpenSearchManager # 타입 힌팅을 위해 필요할 수 있음
import sys # 스트리밍 출력을 위해 추가

def vector_db_search(state: NaiveRAGState) -> NaiveRAGState:
    """
    벡터 데이터베이스 검색을 수행하고 결과를 state['retrieved_documents']에 저장합니다.
    state['opensearch_manager']를 사용하여 검색 로직을 실행합니다.
    state['config']['graph_node_config']['vector_db_search']['search_type']에 따라 검색 유형이 결정됩니다.
    """
    print('='*30)
    print("노드 실행: vector_db_search")
    search_cfg = state['config']['graph_node_config']['vector_db_search']
    opensearch_manager = state['opensearch_manager'] # OpenSearchManager 인스턴스를 가져옵니다.

    index_name = search_cfg['index_name']
    size = search_cfg['size']
    # _source 제외 필드 설정 (dense와 sparse 필드 모두 기본적으로 제외 시도)
    source_excludes = [search_cfg.get('dense_vector_field'), search_cfg.get('sparse_vector_field')]
    source_excludes = [f for f in source_excludes if f is not None] # None 값 제거

    search_type = search_cfg['search_type']
    response = None

    if search_type == 'dense':
        query_embedding = embed_text([state['user_query']])[0]
        response = opensearch_manager.execute_dense_search(
            index_name=index_name,
            query_vector=query_embedding,
            dense_field=search_cfg['dense_vector_field'],
            k=search_cfg['k'],
            size=size,
            source_excludes=source_excludes
        )
    elif search_type == 'sparse':
        tokenized_query = state['sparse_tokenizer'].tokenize(state['user_query'])
        response = opensearch_manager.execute_sparse_search(
            index_name=index_name,
            tokenized_query=tokenized_query,
            sparse_field=search_cfg['sparse_vector_field'],
            size=size,
            source_excludes=source_excludes
        )
    elif search_type == 'hybrid':
        tokenized_query = state['sparse_tokenizer'].tokenize(state['user_query'])
        query_embedding = embed_text([state['user_query']])[0]

        hybrid_search_config = search_cfg['hybrid_search_config']
        normalization = hybrid_search_config['normalization']
        combination = hybrid_search_config['combination']
        weights = hybrid_search_config['weights']
        hybrid_search_pipeline_name = f"{normalization}_{combination}_{'_'.join([str(int(w*10)) for w in weights])}"
        
        response = opensearch_manager.execute_hybrid_search_with_pipeline(
            index_name=index_name,
            pipeline_name=hybrid_search_pipeline_name,
            query_vector=query_embedding,
            dense_field=search_cfg['dense_vector_field'],
            k_dense=search_cfg['k'], # 'k'는 dense 검색의 k로 사용
            tokenized_query=tokenized_query,
            sparse_field=search_cfg['sparse_vector_field'],
            size=size,
            source_excludes=source_excludes
        )
    else:
        # opensearch_manager의 로그와는 별개로, 노드 레벨에서도 오류를 명확히 발생시킵니다.
        raise ValueError(f"지원되지 않는 검색 유형입니다: {search_type}. 'dense', 'sparse', 'hybrid' 중 하나여야 합니다.")

    state['retrieved_documents'] = response['hits']['hits']
    print(f"vector_db_search: {len(state['retrieved_documents'])}개의 문서를 검색했습니다.")
    return state

def generate_answer(state: NaiveRAGState) -> NaiveRAGState:
    """
    검색된 문서를 사용하여 LLM으로부터 답변을 생성합니다.
    결과는 state['llm_answer']에 저장되며, 설정에 따라 스트리밍 출력을 합니다.
    """
    print('='*30)
    print("노드 실행: generate_answer")
    llm_cfg = state['config']['graph_node_config']['generate_answer']
    
    # 검색된 문서가 없는 경우 처리
    if not state.get('retrieved_documents'):
        print("generate_answer: 검색된 문서가 없어 답변 생성을 건너뜁니다.")
        state['llm_answer'] = llm_cfg.get('no_documents_found_answer', "죄송합니다, 관련된 정보를 찾지 못했습니다.")
        state['llm_stream_handled_by_node'] = False # 스트리밍을 하지 않았으므로 False
        return state

    # 문서 포맷팅
    documents_formatted = []
    for doc in state['retrieved_documents']:
        source = doc.get('_source', {})
        file_name = source.get('file_name', '알 수 없는 파일')
        # retrieve_content 대신 text_content 또는 다른 필드 이름을 사용할 수 있으므로 설정에서 가져오도록 고려 가능
        content = source.get(llm_cfg.get('document_content_field', 'retrieve_content'), '내용 없음')
        documents_formatted.append(f'# {file_name}\n\n{content}')
    
    documents_string = "\n\n---\n\n".join(documents_formatted)

    system_prompt = llm_cfg.get('system_prompt_template', "너는 T3Q 회사의 AI 비서야. 사용자의 질문에 대해 친절하고 정확하게 답변해야 해.")
    user_prompt_template = llm_cfg.get('user_prompt_template', """다음은 사용자의 질문과 관련된 문서들이야. 이 문서들을 참고해서 사용자의 질문에 답변해줘.
    문서에 명시적으로 언급되지 않은 내용은 답변에 포함하지 마.

    [사용자 질문]
    {user_query}

    [참고 문서]
    {documents}""")
    
    user_prompt = user_prompt_template.format(user_query=state['user_query'], documents=documents_string)

    should_stream_output = llm_cfg.get('stream_output', False)
    accumulated_response_strings = []

    llm_params = {
        "temperature": llm_cfg.get('temperature', 0.7),
        "top_p": llm_cfg.get('top_p', 0.8),
        "top_k": llm_cfg.get('top_k', 20),
        "repetition_penalty": llm_cfg.get('repetition_penalty', 1.05)
    }

    print("="*15, f"generate_answer: LLM 호출 시작 (스트리밍: {should_stream_output})", "="*15)
    if should_stream_output:
        response_generator = generate_llm_response(
            system_prompt=system_prompt, 
            user_prompt=user_prompt, 
            stream=True, 
            **llm_params
        )
        # 스트리밍 응답 처리: generate_llm_response가 다양한 LLM SDK의 청크를 반환할 수 있으므로,
        # 아래 로직은 일반적인 경우를 다루려고 시도합니다.
        # model_call.py의 generate_llm_response가 반환하는 청크의 정확한 구조에 맞춰 조정하는 것이 가장 좋습니다.
        for chunk_obj in response_generator:
            content_piece = None
            if hasattr(chunk_obj, 'choices') and chunk_obj.choices and \
               hasattr(chunk_obj.choices[0], 'delta') and \
               hasattr(chunk_obj.choices[0].delta, 'content'):
                content_piece = chunk_obj.choices[0].delta.content # OpenAI 유사 API
            elif hasattr(chunk_obj, 'text'): # 일부 API는 chunk.text로 제공
                content_piece = chunk_obj.text
            elif isinstance(chunk_obj, str): # 이미 문자열로 반환되는 경우
                content_piece = chunk_obj
            # 여기에 다른 LLM SDK의 청크 구조에 대한 elif 조건들을 추가할 수 있습니다.
            
            if content_piece:
                print(content_piece, end='', flush=True) 
                accumulated_response_strings.append(content_piece)
            elif chunk_obj is None and not accumulated_response_strings:
                pass # 일부 모델의 초기 빈 청크는 무시

        print() # 스트리밍 완료 후 줄바꿈
        state['llm_answer'] = "".join(accumulated_response_strings)
        state['llm_stream_handled_by_node'] = True
    else:
        full_response = generate_llm_response(
            system_prompt=system_prompt, 
            user_prompt=user_prompt, 
            stream=False, 
            **llm_params
        )
        state['llm_answer'] = full_response
        state['llm_stream_handled_by_node'] = False
    
    print("="*15, "generate_answer: LLM 답변 생성 완료.", "="*15)
    return state