import os, json, time, traceback, hashlib, sys
from opensearchpy import OpenSearch

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) # 상대경로로 root 설정 (Rag_Standard_v2)
sys.path.append(BASE_DIR)
from rag_standard.utils import setup_logger, config_setting, opensearch_manager

global log
log = setup_logger.setup_logger('OpenSearch', 'opensearch')
config_path = os.path.join(BASE_DIR, 'configs', 'main_config.yaml')
config = config_setting.load_yaml_config(config_path)
config_setting.load_env()

def get_unique_id(base_string, index_name):
    # 주어진 문자열로부터 MD5 해시를 생성 (초기 id)
    base_id = hashlib.md5(base_string.encode('utf-8')).hexdigest()
    unique_id = base_id
    counter = 1

    # 해당 id가 존재하면, 카운터를 추가해서 고유 id를 생성
    while client.exists(index=index_name, id=unique_id):
        unique_id = f"{base_id}_{counter}"
        counter += 1
    return unique_id

class OpenSearchHelper:
    """ OpenSearch Vector DB에 index을 업로드하기 위한 클래스 """
    def __init__(self):
        self.client = opensearch_manager.OpenSearchManager(os.getenv("OPENSEARCH_HOST"), os.getenv("OPENSEARCH_PORT"))

    def make_index(self, index_name):
        """ OpenSearch 컬렉션 생성 함수 (없는 경우에만 생성) """
        global log

        settings = {
            "number_of_shards":"5", # 처음에 세팅하면 변경 불가. 새로 인덱스 정의해야함
            "number_of_replicas":"5", # 나중에 변경 가능
            "index": {
                "knn": True,  
                "knn.algo_param":{"ef_search":512},
            },
            "analysis": {
                "analyzer": { 
                    "lowercase_analyzer": {   
                        "type": "custom",
                        "tokenizer":"standard" , 
                        "filter":["lowercase"] 
                    }
                }
            },
        }
        mappings = {
            "properties": {
                "file_type": {"type": "text"},
                "file_name": {"type": "text"},
                "extension": {"type": "text"},
                "chunk_order": {"type": "text"},
                "chunk_name": {"type": "text"},
                "filtering_id": {"type": "text"},
                "retrieve_content": {"type": "text"},
                "retrieve_token_count": {"type": "integer"},
                "llm_content": {"type": "text"},
                "llm_token_count": {"type": "integer"},
                "file_size": {"type": "integer"},
                "text_sparse_kiwi": {"type": "text"},
                "text_dense": {  
                    "type": "knn_vector",
                    "dimension": 1024, # bge-m3    
                    "method": {  
                        "name": "hnsw", 
                        "engine": "nmslib", 
                        "space_type": "cosinesimil",
                        "parameters": {
                            "ef_construction": 512, 
                            "m": 22 
                        }
                    }
                }
            }
        }
        client.create_index(index_name = index_name, mapping = mappings, settings = settings)
        
    def upload_data(self, mod_meta, save_path):
        """ 임베딩 데이터를 OpenSearch 벡터 데이터베이스에 업로드하는 함수 """
        global log
        log = setup_logger()

        index_name = config['db_settings']['opensearch_index'] # OpenSearch index명

        log.info("Processing OpenSearch...")
        start_time = time.time()
        try:
            # 컬렉션 생성 또는 확인
            res = self.make_index(index_name)
            if not res:
                return False

            # 각 메타데이터 항목을 처리하여 OpenSearch에 업로드
            for m in mod_meta:
                opensearch_path = f"{save_path}/OpenSearch/{m['file_name']}.json"
                os.makedirs(os.path.dirname(opensearch_path), exist_ok=True)

                # 기존 JSON 파일이 있으면 불러오기, 없으면 빈 리스트로 시작
                if os.path.exists(opensearch_path):
                    with open(opensearch_path, "r", encoding="utf-8-sig") as f:
                        try:
                            existing_data = json.load(f)  # 기존 데이터 불러오기
                            if not isinstance(existing_data, list):  
                                existing_data = [existing_data]  # 기존 데이터가 리스트가 아닐 경우 리스트로 변환
                        except json.JSONDecodeError:
                            existing_data = []  # JSON 파일이 비어 있거나 손상된 경우 빈 리스트로 초기화
                else:
                    existing_data = []  # 파일이 없으면 빈 리스트로 시작
                
                if m['retrieve_token_count'] != 0: # 토큰이 있는 경우만 처리
                    # 키 이름을 확인: 만약 실제 데이터에 'text_dense' 키가 존재한다면 그걸 사용
                    dense_vector = m.get('text-dense')  # 또는 m.get('text_dense')
                    if dense_vector is None:
                        log.error("문서 [%s]의 text_dense 값이 None입니다. 해당 문서를 건너뜁니다.", m['filtering_id'])
                        continue
            
                    # 고유한 id 생성
                    new_id = get_unique_id(m['filtering_id'], index_name)

                    body = {           
                        "id": new_id,         
                        "project_name": m['project_name'],
                        "file_name": m['file_name'],
                        "extension": m['extension'],
                        "chunk_order": m['chunk_order'],
                        "chunk_name": m['chunk_name'],
                        "filtering_id": m['filtering_id'],
                        "retrieve_content": m['retrieve_content'],
                        "retrieve_token_count": m['retrieve_token_count'],
                        "llm_content": m['llm_content'],
                        "llm_token_count": m['llm_token_count'],
                        "file_size": m['file_size'],
                        "text_sparse_kiwi": m['text-sparse'],
                        "text_dense": dense_vector #m['text-dense']
                    }
                    existing_data.append(body)

                    # 메타데이터를 JSON 파일로 저장 (덮어씌우지 않고 누적 저장)
                    with open(opensearch_path, "w", encoding="utf-8-sig") as f:
                        json.dump(existing_data, f, ensure_ascii=False, indent=2)
        
                    log.info(f"[OpenSearch] Embedding data saved at {opensearch_path}")
            
                    client.index(index=index_name, id=new_id, body=body)

            log.info(f"Finished inserting data to {index_name} - {new_id}")

        except Exception as e:
            log.error(f"Error uploading data: {traceback.format_exc()}")
            raise

        finally:
            end_time = time.time() - start_time
            log.info("Finished processing OpenSearch - Time spent: %.2f seconds", end_time)
            return True