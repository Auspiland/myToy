import os, json, time, traceback, hashlib, uuid, sys
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) # 상대경로로 root 설정 (Rag_Standard_v2)
sys.path.append(BASE_DIR)
from rag_standard.utils import setup_logger, config_setting

global log
log = setup_logger.setup_logger('Qdrant', 'qdrant')
config_path = os.path.join(BASE_DIR, 'configs', 'main_config.yaml')
config = config_setting.load_yaml_config(config_path)

class QdrantHelper:
    """ Qdrant Vector DB에 collection을 업로드하기 위한 클래스 """
    def __init__(self):
        self.client = self.client_connect()

    def client_connect(self):
        """ Qdrant 클라이언트 연결 설정 함수 """
        global client
        client = QdrantClient(host=config['db_settings']['qdrant_host'], port=config['db_settings']['qdrant_port'], timeout = 999999)
        return client

    def check_collection(self, collection_name):
        """ 컬렉션 존재 여부 확인 함수 """
        try:
            self.client.get_collection(collection_name = collection_name)
        except Exception as e:
            return False
        else:
            return True

    def make_collection(self, collection_name):
        """ Qdrant 컬렉션 생성 함수 (없는 경우에만 생성) """
        global log
        
        if self.check_collection(collection_name):
            log.info("Collection exists")
            return True
        else:
            log.info("Creating collection...")
            try:
                self.client.create_collection(
                    collection_name = collection_name,
                    vectors_config = {
                        "text-dense": models.VectorParams(
                            size=1024,
                            distance = models.Distance.COSINE
                        ),
                    },
                    sparse_vectors_config = {
                        "text-sparse": models.SparseVectorParams(),
                    }
                )
                log.info("Creating collection success.")
            except Exception as e:
                raise e
            else:
                return True

    def check_existing_point(self, filtering_id: str, project_name: str, collection_name: str):
        """
        주어진 filtering_id와 project_name으로 컬렉션에서 포인트의 존재 여부 확인
        
        Args:
            filtering_id (str): 검색할 고유 식별자 (파일명_페이지)
            project_name (str): 파일 유형
            collection_name (str): Qdrant 컬렉션 이름
        
        Returns:
            Tuple: (존재 여부, 포인트 ID, 현재 버전, 페이로드)
                - exists (bool): 포인트 존재 여부
                - point_id (int): 존재하는 경우 포인트 ID
                - version (int): 현재 버전
                - payload (dict): 포인트의 페이로드 데이터
        """
        try:
            # filtering_id와 project_name이 일치하는 포인트 검색
            search_result = client.scroll(
                collection_name=collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="filtering_id",
                            match=MatchValue(value=filtering_id)
                        ),
                        FieldCondition(
                            key="project_name",
                            match=MatchValue(value=project_name)
                        )
                    ]
                ),
                limit=1 # 첫 번째 일치하는 포인트만 가져옴
            )
            
            points = search_result[0]  # 첫 번째 요소는 포인트들, 두 번째는 다음 페이지 오프셋
            if points and len(points) > 0:
                point = points[0]
                if (
                    point.payload.get('filtering_id') == filtering_id
                    and point.payload.get('project_name') == project_name
                ):
                    current_version = point.payload.get('version', 0) # 현재 버전 정보 확인
                    log.info(f"Found existing point with filtering_id {filtering_id} - {project_name}, current version: {current_version}")
                    return True, point.id, current_version, point.payload # 포인트 존재 시 관련 정보 반환
            return False, None, None, None # 포인트가 없는 경우
            
        except Exception as e:
            log.error(f"Error checking existing point: {e}")
            raise

    def generate_point_id(self, seed: str, collection_name: str) -> str:
        """
        주어진 seed 값을 사용하여 고유한 포인트 ID를 생성하고,
        Qdrant에서 중복 여부를 확인한 후 충돌이 발생하면 새로운 ID를 생성함
        
        Args:
            seed: ID를 생성할 기준이 되는 문자열
            collection_name: Qdrant에서 확인할 컬렉션 이름
        
        Returns:
            고유한 포인트 ID (중복이 없는 ID)
        """
        while True:
            # 입력받은 seed 문자열로 해시값 생성
            hash_object = hashlib.sha256(seed.encode())
            # 해시값의 앞 16자리를 16진수 정수로 변환하여 ID로 사용
            unique_id = int(hash_object.hexdigest()[:16], 16)
    
            # Qdrant 컬렉션에서 해당 ID의 존재 여부 확인
            try:
                existing_point = client.retrieve(
                    collection_name=collection_name,
                    ids=[unique_id]
                )
                # ID가 이미 존재하는 경우, 무작위 숫자를 추가하여 새로운 seed 생성
                if existing_point:
                    log.info(f"ID {unique_id} already exists, generating new seed.")
                    seed = seed + str(uuid.uuid4()) # random.randint(0, 10000))
                else:
                    # 중복되지 않은 ID 발견 시 반환
                    log.info(f"ID {unique_id} considered unique. Returning it.")
                    return unique_id
            except Exception as e:
                # 해당 ID가 없는 경우(예외 발생), 해당 ID를 고유한 것으로 간주하고 반환
                return unique_id
        
    def upload_data(self, mod_meta, save_path):
        """ 임베딩 데이터를 Qdrant 벡터 데이터베이스에 업로드하는 함수 """
        global log
        log = setup_logger()

        collection_name = config['db_settings']['qdrant_collection'] # Qdrant collection명
        pname = config['data_processing_settings']['version_name']

        log.info("Processing Qdrant...")
        qdrant_start_time = time.time()
        try:
            # 컬렉션 생성 또는 확인
            res = self.make_collection(collection_name)
            if not res:
                return False

            log.info(f"[Qdrant] Embedding data saved at {save_path}")
            
            # 각 메타데이터 항목을 처리하여 Qdrant에 업로드
            for m in mod_meta:
                qdrant_path = f"{save_path}/Qdrant/{m['file_name']}.json"
                os.makedirs(os.path.dirname(qdrant_path), exist_ok=True)
                with open(qdrant_path, "w", encoding="utf-8-sig") as f:
                    json.dump(mod_meta, f, ensure_ascii=False, indent=2)
                                
                if m['retrieve_token_count'] != 0: # 토큰이 있는 경우만 처리
                    exists, existing_id, current_version, current_payload = self.check_existing_point(m['filtering_id'], pname, collection_name) # 기존 포인트 확인
    
                    if exists and current_payload.get('project_name') == pname:
                        # Only reuse the ID if BOTH filtering_id AND project_name match
                        seed_id = existing_id
                        new_version = (current_version or 0) + 1
                        log.info(f"Same document found. Incrementing version from {current_version} to {new_version}")
                    else:
                        # Use new ID for different file types
                        seed_id = self.generate_point_id(m.get('file_name'), collection_name)
                        new_version = 1
                        log.info("New document. Creating with initial version.")
    
                    cop_m = m.copy() # 원본 메타데이터 복사
                    
                    # 메타데이터 업데이트 및 임베딩 생성 준비
                    cop_m['version'] = new_version
                    updated_at = str(datetime.now())
                    cop_m.update({'updated_at': updated_at})

                    # 벡터 데이터 분리
                    dv = cop_m.pop('text-dense') # 밀집 벡터
                    sv = cop_m.pop('text-sparse') # 희소 벡터

                    # Qdrant에 포인트 업로드
                    self.client.upsert(
                        collection_name = collection_name,
                        points = [
                            models.PointStruct(
                                id = seed_id,
                                payload = cop_m, # 메타데이터를 페이로드로 저장
                                vector = {
                                    "text-dense": dv,
                                    "text-sparse": models.SparseVector(indices=sv['indices'], values=sv['values']),
                                }
                            )
                        ]
                    )
                # 결과 로깅
                if exists:
                    log.info(f"Updated version for duplicate document. ID: {seed_id}, Version: {new_version}")
                else:
                    log.info(f"Created new document. ID: {seed_id}, Version: {new_version}")

                # 최종 처리 결과 로깅
                log_message = "Updated" if exists else "Created"
                log.info(f"{log_message} document {seed_id} with filtering_id {cop_m['filtering_id']} (Version {cop_m['version']})")

        except Exception as e:
            log.error(f"Error uploading data: {traceback.format_exc()}")
            raise

        finally:
            qdrant_time = time.time() - qdrant_start_time
            log.info("Finished processing Qdrant - Time spent: %.2f seconds", qdrant_time)
            return True