# -*- coding: utf-8 -*-
import json, os, re, requests, traceback, time, sys
from . import qdrant_final, opensearch_final
from kiwipiepy import Kiwi
from fastembed import SparseTextEmbedding
from setproctitle import setproctitle
from tqdm import tqdm

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) # 상대경로로 root 설정 (Rag_Standard_v2)
sys.path.append(BASE_DIR)
from rag_standard.utils import setup_logger, config_setting, sparse_tokenizer

setproctitle("YewonLee/nlp/Embedding")

global log
log = setup_logger.setup_logger('Embedding', 'embedding')

config_path = os.path.join(BASE_DIR, 'configs', 'main_config.yaml')
config = config_setting.load_yaml_config(config_path)

kiwi_config_path = os.path.join(BASE_DIR, 'configs', 'naive_rag_workflow.yaml')
kiwi_config = config_setting.load_yaml_config(kiwi_config_path)

config_setting.load_env()

qdrt = qdrant_final.QdrantHelper()
opsrch = opensearch_final.OpenSearchHelper()

def to_boolean(value):
    """ 문자열을 boolean 값으로 변환하는 함수 """
    # 이미 불리언이면 그대로 반환
    if isinstance(value, bool):
        return value
    # 문자열인 경우, 소문자로 변환한 후 True에 해당하는 값이면 True 반환
    if isinstance(value, str):
        value_lower = value.strip().lower()
        if value_lower in ['true', '1', 't', 'yes', 'y']:
            return True
        elif value_lower in ['false', '0', 'f', 'no', 'n']:
            return False
        else:
            raise ValueError(f"불리언으로 변환할 수 없는 문자열: {value}")
    # 기타 자료형은 내장 bool() 함수를 사용해 변환
    return bool(value)

def calculate_embed(md, qdrant_tf=False):
    """
    문서 메타데이터 리스트에 대한 임베딩(벡터) 계산 함수
    
    Args:
        md (list): 메타데이터 객체 리스트
        
    Returns:
        list: 임베딩이 추가된 메타데이터 리스트
    """
    embed = embedd()
    result_metas = []

    try:
        # 모든 메타데이터의 내용을 한 번에 처리하도록 수정
        input_data = {"contents": [meta['retrieve_content'] for meta in md]}

        if qdrant_tf:
            # 밀집 벡터(dense)와 희소 벡터(sparse) 임베딩 생성
            dense, sparse = embed.embed_doc_qdrant(input_data)
            
            # 오류 발생 시 None 체크
            if dense is None or sparse is None:
                log.error("[Qdrant] Embedding 반환값 중 dense 또는 sparse 벡터가 None 입니다.")
                return result_metas

            log.info("[Qdrant] Dense vectors count: %d", len(dense))
            log.info("[Qdrant] Sparse vectors count: %d", len(sparse))

            # 각 메타데이터, 밀집 벡터, 희소 벡터를 묶어서 처리
            for idx, (meta, dv, sv) in enumerate(zip(md, dense, sparse)):
                enriched_meta = meta.copy() # 원본 메타데이터 복사
                enriched_meta['text-dense'] = dv # 밀집 벡터 추가
                enriched_meta['text-sparse'] = {"indices": sv[0], "values": sv[1]} # 희소 벡터 추가
                result_metas.append(enriched_meta) # 결과 리스트에 추가
            
        else:
            dense, sparse = embed.embed_doc_opensearch(input_data)
            
            if dense is None or sparse is None:
                log.error("[OpenSearch] Embedding 반환값 중 dense 또는 sparse 벡터가 None 입니다.")
                return result_metas
            
            log.info("[OpenSearch] Dense vectors count: %d", len(dense))
            log.info("[OpenSearch] Sparse vectors count: %d", len(sparse))

            # 각 메타데이터, 밀집 벡터, 희소 벡터를 묶어서 처리
            for idx, (meta, dv, sv) in enumerate(zip(md, dense, sparse)):
                enriched_meta = meta.copy() # 원본 메타데이터 복사
                enriched_meta['text-dense'] = dv # 밀집 벡터 추가
                enriched_meta['text-sparse'] = sv # 희소 벡터 추가
                result_metas.append(enriched_meta) # 결과 리스트에 추가
            
    except Exception as e:
        log.error(traceback.format_exc())
            
    return result_metas # 임베딩이 추가된 메타데이터 반환

class BM25:
    """ BM25 기반 희소 벡터 임베딩을 위한 클래스 """
    def __init__(self):
        self.model = SparseTextEmbedding('Qdrant/bm25') # BM25 임베딩 모델 초기화
        # 한국어 형태소 분석기 초기화
        self.kiwi = sparse_tokenizer.KiwiTokenizer(kiwi_config['tokenizer']['included_pos_tags'], kiwi_config['tokenizer']['dictionary_path'])

    def tokenize(self, content):
        """ 텍스트 내용을 토큰화하는 함수 - 공백으로 구분된 토큰 문자열 반환 """
        # 줄바꿈으로 분리된 내용을 처리
        content = content.split('\n')
        content = list(map(lambda x: x.strip(), content))
        content = ''.join(content)
        content = re.sub('\n', ' ', content) # 남은 줄바꿈을 공백으로 변환
        clean = re.sub('\W', ' ', content) # 특수문자 제거

        result = self.kiwi.tokenize(clean)
        # tokens = []
        # # 명사, 미등록어, 외국어, 고유명사만 추출
        # for t in result:
        #     #if t.tag in ["NNG", "UN", "SL", "NNP"]:
        #     tokens.append(t.form)

        # 리스트로 분리하여 join
        tokens = result.split()
            
        return ' '.join(tokens)
        
    def bm25_embed(self, text):
        """
        텍스트에 대한 BM25 희소 벡터 임베딩 생성 함수
        
        Args:
            text (str): 임베딩할 텍스트
            
        Returns:
            tuple: (인덱스 리스트, 값 리스트) 형태의 희소 벡터
        """
        tokenized = self.tokenize(text) # 텍스트 토큰화

        # BM25 모델을 사용하여 임베딩 생성
        embed_res = self.model.embed(tokenized)
        result = list(embed_res)[0].as_object()

        # 인덱스와 값을 리스트로 변환하여 반환
        return result['indices'].tolist(), result['values'].tolist()
    

class embedd:
    """ 문서 임베딩을 위한 클래스 (밀집 벡터와 희소 벡터 모두 처리) """
    def __init__(self):
        self.bm25 = BM25() # BM25 객체 초기화
    
    def embed_doc_qdrant(self, metadata):
        """
        문서 내용에 대한 임베딩(밀집 벡터 및 희소 벡터) 생성 함수 - Qdrant용
        Qdrant의 경우 희소/밀집 벡터 값을 계산한 결과를 바로 저장
        
        Args:
            metadata (dict): 문서 내용이 포함된 메타데이터 (retrieve_content 키에 텍스트 리스트가 있어야 함)
            
        Returns:
            tuple: (밀집 벡터 리스트, 희소 벡터 리스트)
        """
        log.info('[Qdrant] Calling embed document')
        input_data = {"text": metadata['contents'], "mode": "korean"} # API 요청용 데이터 구성

        # 밀집 벡터(Dense) 생성 - BGE 모델 사용
        log.info('[Qdrant] [DENSE] Call BGE embedding...')
        log.info('[Qdrant] Before API Request')
        api_response = requests.post(os.getenv("TEXT_EMBEDDING_API_URL"), json=input_data, timeout=999999)
        log.info('[Qdrant] After API Request')

        # API 응답 확인 및 처리
        if api_response.status_code != 200:
            log.error(f"[Qdrant] API Error: {api_response.status_code} - {api_response.text}")
            return None, None
        try:
            api_response = json.loads(api_response.content.decode())[0]
        except json.JSONDecodeError as e:
            log.error(f"[Qdrant] JSON Decode Error: {e}")
            return None, None
            
        dense_vec = api_response # 밀집 벡터 저장

        # 희소 벡터(Sparse) 생성 - BM25 모델 사용
        sparse_result = []
        log.info('[Qdrant] [SPARSE] Call BM25 embedding...')
        for c in input_data['text']:
            try:
                sparse_idx, sparse_val = self.bm25.bm25_embed(c) # BM25 임베딩 생성
                sparse_result.append([sparse_idx, sparse_val])
            except Exception as e:
                log.error(f"[Qdrant] Sparse Embedding Error: {e}")
                sparse_result.append([[], []]) # 오류 발생 시 빈 벡터 추가
            
        log.info("[Qdrant] Returning Result")
        return dense_vec, sparse_result # 밀집 벡터와 희소 벡터 리스트 반환
    
    def embed_doc_opensearch(self, metadata):
        """
        문서 내용에 대한 임베딩(밀집 벡터 및 희소 벡터) 생성 함수 - OpenSearch용
        OpenSearch의 경우 밀집 벡터는 계산한 값을 저장하지만, 희소 벡터는 토크나이징한 내용을 저장함
        
        Args:
            metadata (dict): 문서 내용이 포함된 메타데이터 (retrieve_content 키에 텍스트 리스트가 있어야 함)
            
        Returns:
            tuple: (밀집 벡터 리스트, 희소 벡터 리스트)
        """
        log.info('[OpenSearch] Calling embed document')
        input_data = {"text": metadata['contents'], "mode": "korean"} # API 요청용 데이터 구성

        # 밀집 벡터(Dense) 생성 - BGE 모델 사용
        log.info('[OpenSearch] [DENSE] Call BGE embedding...')
        log.info('[OpenSearch] Before API Request')
        api_response = requests.post(os.getenv("TEXT_EMBEDDING_API_URL"), json=input_data, timeout=999999)
        log.info('[OpenSearch] After API Request')

        # API 응답 확인 및 처리
        if api_response.status_code != 200:
            log.error(f"[OpenSearch] API Error: {api_response.status_code} - {api_response.text}")
            return None, None
        try:
            api_response = json.loads(api_response.content.decode())[0]
        except json.JSONDecodeError as e:
            log.error(f"[OpenSearch] JSON Decode Error: {e}")
            return None, None
            
        dense_vec = api_response # 밀집 벡터 저장

        # 희소 벡터(Sparse) 생성 - Kiwi 토크나이저 사용용
        sparse_result = []
        log.info('[OpenSearch] [SPARSE] Start Kiwi tokenizing...')
        for c in input_data['text']:
            try:
                tokenized_text = self.bm25.tokenize(c)
                sparse_result.append(tokenized_text)
            except Exception as e:
                log.error(f"[OpenSearch] Kiwi Tokenizing Error: {e}")
                sparse_result.append('') # 오류 발생 시 빈 벡터 추가
            
        log.info("[OpenSearch] Returning Result")
        return dense_vec, sparse_result # 밀집 벡터와 희소 벡터 리스트 반환

def main():
    """ 메인 실행 함수 - 임베딩해서 데이터베이스에 업로드하는 과정 관리 """
    calculated = False

    log.info("Getting info from path.json")

    pname = config['data_processing_settings']['version_name']
    root_path = config['data_processing_settings']['root_path']
    meta_path = f"{root_path}/{pname}/Split" # 결과 저장되어 있는 폴더
    save_path = f"{root_path}/{pname}/Embedding" # 임베딩 결과물이 저장될 폴더 경로
    qdrant_ = config['data_processing_settings']['qdrant_tf'] # Qdrant 사용할 건지 여부
    
    log.info(f"Got Target path: {meta_path}")
    qdrant_tf = to_boolean(qdrant_)
    
    log.info("Starting Process...")
    overall_start = time.time()
    all_db_uploaded = True

    # 1. 임베딩 벡터 계산 단계
    try:
        log.info("Calculating vectors")
        vector_start = time.time()
        for root, dirs, files in os.walk(meta_path):
            # '.ipynb_checkpoints' 폴더 제외
            dirs[:] = [d for d in dirs if d != '.ipynb_checkpoints']
            for file in tqdm(files, desc=f"Processing files in {root}", unit="file"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8-sig") as f:
                    metas = json.load(f)
                mod_meta = calculate_embed(metas, qdrant_tf)
                if not mod_meta:
                    log.error("Embedding calculation failed for file: " + path)
                    continue
                    
                vector_time = time.time() - vector_start
                log.info("Finished calculating vectors - Time: %2f seconds", vector_time)

                if qdrant_tf:
                    # 2-1. 데이터베이스 업로드 단계 (Qdrant)
                    try:
                        log.info("[Qdrant] Uploading to DB for file: " + path)
                        embed_start = time.time()
                        db_uploaded = qdrt.upload_data(mod_meta, save_path)
                        if not db_uploaded:
                            log.error("[Qdrant] DB upload failed for file: " + path)
                            all_db_uploaded = False
                        embed_time = time.time() - embed_start
                        log.info("[Qdrant] Finished uploading to DB - Time: %2f seconds", embed_time)
                    except Exception as e:
                        log.error(traceback.format_exc())
                        all_db_uploaded = False
                else:
                    # 2-2. 데이터베이스 업로드 단계 (OpenSearch)
                    try:
                        log.info("[OpenSearch] Uploading to DB for file: " + path)
                        load_start = time.time()
                        db_uploaded = opsrch.upload_data(mod_meta, save_path)
                        if not db_uploaded:
                            log.error("[OpenSearch] DB upload failed for file: " + path)
                            all_db_uploaded = False
                        ttl_time = time.time() - load_start
                        log.info("[OpenSearch] Finished uploading to DB - Time: %2f seconds", ttl_time)
                    except Exception as e:
                        log.error(traceback.format_exc())
                        all_db_uploaded = False                        
                    
    except Exception as e:
        log.error(traceback.format_exc())
    else:
        calculated = True
        
    assert calculated == True, 'Embed calculation Failed.'
    assert all_db_uploaded == True, 'DB upload Failed.'

    # 전체 실행 시간 계산
    overall_time = time.time() - overall_start
    log.info("Overall time processed: %2f seconds", overall_time)

if __name__ == '__main__':
    pname = config['data_processing_settings']['version_name']
    root_path = config['data_processing_settings']['root_path']
    meta_path = f"{root_path}/{pname}/Split"
    save_path = f"{root_path}/{pname}/Embedding"
    kiwi_dic = kiwi_config['tokenizer']['dictionary_path']
    qdrant_ = config['data_processing_settings']['qdrant_tf']
    index_name = config['db_settings']['opensearch_index']
    qdrant_name = config['db_settings']['qdrant_collection']

    # 호출된 정보들 확인
    print(f"Project Name: {pname}\nQdrant Collection Name: {qdrant_name}\nTarget Path: {meta_path}\nEmbedding path: {save_path}\nOpenSearch Index Name: {index_name}\nWhether upload to Qdrant: {qdrant_tf}\nIf there's a dictionary for kiwi tokenizer: {kiwi_dic}")

    main()