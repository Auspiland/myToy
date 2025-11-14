# rag_standard/utils/opensearch_manager.py
from opensearchpy import OpenSearch, exceptions as opensearch_exceptions
from rag_standard.utils.setup_logger import setup_logger # 동일 디렉토리에 log_setup.py가 있다고 가정
from typing import List

# 이 모듈을 위한 로거
log = setup_logger('OpenSearchManager', 'opensearch_manager')

class OpenSearchManager:
    """
    OpenSearch 연결 및 관리를 위한 클래스입니다.

    OpenSearch 클러스터에 연결하고, 인덱스 및 검색 파이프라인을 관리하는
    메서드를 제공합니다.
    """
    def __init__(self, host: str, port: int | str, http_auth=None):
        """
        OpenSearchManager 인스턴스를 초기화합니다.

        Args:
            host (str): OpenSearch 호스트 주소입니다.
            port (int | str): OpenSearch 포트 번호입니다.
            http_auth (tuple, optional): HTTP 인증을 위한 사용자 이름과 비밀번호 튜플입니다.
                                       예: ('admin', 'admin'). 기본값은 None입니다.

        Raises:
            ValueError: 호스트 또는 포트가 제공되지 않은 경우 발생합니다.
        """
        if not host or not port:
            log.error("OpenSearch 호스트 또는 포트가 제공되지 않았습니다.")
            raise ValueError("OpenSearch 호스트와 포트는 필수입니다.")

        self.host = host
        self.port = port
        self.http_auth = http_auth # 예: ('admin', 'admin')
        self.client = self._connect()

    def _connect(self) -> OpenSearch:
        """
        OpenSearch 클러스터에 연결을 시도합니다.

        Returns:
            OpenSearch: 성공적으로 연결된 OpenSearch 클라이언트 객체입니다.

        Raises:
            ConnectionError: OpenSearch에 핑을 실패하거나 연결 중 오류가 발생한 경우 발생합니다.
        """
        try:
            client = OpenSearch(
                hosts=[{'host': self.host, 'port': self.port}],
                http_auth=self.http_auth,
                use_ssl=True if str(self.port) == '443' else False, # 기본 SSL 가정
                verify_certs=True, # 환경에 맞게 조정하세요
                ssl_assert_hostname=False, # 환경에 맞게 조정하세요
                ssl_show_warn=False # 환경에 맞게 조정하세요
            )
            if client.ping():
                log.info(f"OpenSearch에 성공적으로 연결되었습니다 ({self.host}:{self.port})")
                return client
            else:
                log.error(f"OpenSearch 핑 실패 ({self.host}:{self.port})")
                raise ConnectionError(f"OpenSearch 핑 실패 ({self.host}:{self.port})")
        except Exception as e:
            log.error(f"OpenSearch 연결 중 오류 발생: {e}")
            raise

    def get_client(self) -> OpenSearch:
        """
        현재 OpenSearch 클라이언트 객체를 반환합니다.

        Returns:
            OpenSearch: OpenSearch 클라이언트 객체입니다.
        """
        return self.client

    def index_exists(self, index_name: str) -> bool:
        """
        지정된 이름의 인덱스가 OpenSearch에 존재하는지 확인합니다.

        Args:
            index_name (str): 확인할 인덱스의 이름입니다.

        Returns:
            bool: 인덱스가 존재하면 True, 그렇지 않으면 False를 반환합니다.
                  오류 발생 시 False를 반환합니다.
        """
        try:
            return self.client.indices.exists(index=index_name)
        except Exception as e:
            log.error(f"인덱스 '{index_name}' 존재 여부 확인 중 오류 발생: {e}")
            return False # 오류 발생 시 존재하지 않는 것으로 가정

    def create_index(self, index_name: str, mapping: dict, settings: dict = None):
        """
        지정된 이름, 매핑 및 설정으로 OpenSearch에 새 인덱스를 생성합니다.

        인덱스가 이미 존재하면 생성을 시도하지 않습니다.

        Args:
            index_name (str): 생성할 인덱스의 이름입니다.
            mapping (dict): 인덱스의 매핑 정의입니다.
            settings (dict, optional): 인덱스의 설정입니다. 기본값은 None입니다.

        Returns:
            bool: 인덱스가 성공적으로 생성되었거나 이미 존재하면 True를 반환합니다.

        Raises:
            Exception: 인덱스 생성 중 예상치 못한 오류가 발생한 경우 발생합니다.
        """
        if self.index_exists(index_name):
            log.info(f"인덱스 '{index_name}'이(가) 이미 존재합니다.")
            return True

        index_body = {}
        if settings:
            index_body["settings"] = settings
        if mapping:
            index_body["mappings"] = mapping

        try:
            log.info(f"인덱스 '{index_name}' 생성 중, 내용: {index_body}")
            response = self.client.indices.create(index=index_name, body=index_body)
            log.info(f"인덱스 '{index_name}'이(가) 성공적으로 생성되었습니다: {response}")
            return True
        except opensearch_exceptions.RequestError as e:
            if e.error == 'resource_already_exists_exception':
                log.info(f"인덱스 '{index_name}'이(가) 이미 존재합니다 (경쟁 조건 감지).")
                return True
            log.error(f"인덱스 '{index_name}' 생성 실패: {e}")
            raise
        except Exception as e:
            log.error(f"인덱스 '{index_name}' 생성 중 예상치 못한 오류 발생: {e}")
            raise

    def check_search_pipeline(self, pipeline_name: str) -> bool:
        """
        OpenSearch에 지정된 이름의 검색 파이프라인이 존재하는지 확인합니다.

        Args:
            pipeline_name (str): 확인할 검색 파이프라인의 이름입니다.

        Returns:
            bool: 파이프라인이 존재하면 True를 반환합니다.
        """
        try:
            self.client.transport.perform_request(
                method="GET",
                url=f"/_search/pipeline/{pipeline_name}"
            )
            return True
        except opensearch_exceptions.TransportError as e:
            return False


    def create_search_pipeline(self, pipeline_name: str, normalization: str, combination: str, weights: List[float]):
        """
        OpenSearch에 검색 파이프라인을 생성하거나 업데이트합니다.

        OpenSearch는 파이프라인 존재 여부를 직접 확인하는 API를 제공하지 않으므로,
        GET 요청을 통해 확인 후 생성/업데이트를 시도합니다.

        Args:
            pipeline_name (str): 생성하거나 업데이트할 검색 파이프라인의 이름입니다.
            pipeline_definition (dict): 검색 파이프라인의 정의입니다.

        Returns:
            bool: 파이프라인이 성공적으로 생성 또는 업데이트되면 True를 반환합니다.

        Raises:
            Exception: 파이프라인 생성 또는 업데이트 중 오류가 발생한 경우 발생합니다.
        """

        pipeline_definition = {
        "description": f"Post processor for hybrid search. normalization: {normalization}, combination: {combination}, weights: {weights}",
        "phase_results_processors": [
            {
            "normalization-processor": {
                "normalization": {
                "technique": normalization
                },
                "combination": {
                "technique": combination,
                "parameters": {
                    "weights": weights
                }
                }
            }
            }
        ]
        }

        try:
            response = self.client.transport.perform_request(
                method="PUT",
                url=f"/_search/pipeline/{pipeline_name}",
                body=pipeline_definition
            )
            log.info(f"검색 파이프라인 '{pipeline_name}'이(가) 성공적으로 생성/업데이트되었습니다: {response}")
            return True
        except Exception as e:
            log.error(f"검색 파이프라인 '{pipeline_name}' 생성/업데이트 실패: {e}")
            raise

    # ===================
    # 검색 관련 메서드
    # ===================
    def execute_dense_search(self, index_name: str, query_vector: list, dense_field: str, k: int, size: int, source_excludes: list = None) -> dict:
        """
        Dense 벡터 검색을 수행합니다.

        Args:
            index_name (str): 검색할 인덱스 이름입니다.
            query_vector (list): 쿼리 텍스트의 임베딩 벡터입니다.
            dense_field (str): dense 벡터가 저장된 필드 이름입니다.
            k (int): KNN 검색에서 찾을 이웃의 수입니다.
            size (int): 반환할 결과의 최대 개수입니다.
            source_excludes (list, optional): 결과의 `_source` 필드에서 제외할 필드 목록입니다.

        Returns:
            dict: OpenSearch 검색 결과입니다.
        """
        log.info(f"Dense 검색 실행: 인덱스='{index_name}', k={k}, size={size}")
        search_data = {
            "size": size,
            "_source": {"excludes": source_excludes or []},
            "query": {
                "knn": {
                    dense_field: {
                        "vector": query_vector,
                        "k": k
                    }
                }
            }
        }
        try:
            response = self.client.search(index=index_name, body=search_data)
            return response
        except Exception as e:
            log.error(f"Dense 검색 중 오류 발생 (인덱스: {index_name}): {e}")
            raise

    def execute_sparse_search(self, index_name: str, tokenized_query: str, sparse_field: str, size: int, source_excludes: list = None) -> dict:
        """
        Sparse 벡터 (keyword, BM25 등) 검색을 수행합니다.

        Args:
            index_name (str): 검색할 인덱스 이름입니다.
            tokenized_query (str): 토큰화된 쿼리 문자열입니다.
            sparse_field (str): sparse 벡터/토큰이 저장된 필드 이름입니다.
            size (int): 반환할 결과의 최대 개수입니다.
            source_excludes (list, optional): 결과의 `_source` 필드에서 제외할 필드 목록입니다.

        Returns:
            dict: OpenSearch 검색 결과입니다.
        """
        log.info(f"Sparse 검색 실행: 인덱스='{index_name}', size={size}")
        search_data = {
            "size": size,
            "_source": {"excludes": source_excludes or []},
            "query": {
                "match": {
                    sparse_field: tokenized_query
                }
            }
        }
        try:
            # DFS_QUERY_THEN_FETCH는 정확도를 높일 수 있으나 성능에 영향을 줄 수 있습니다. 필요에 따라 사용합니다.
            response = self.client.search(index=index_name, params={"search_type": "dfs_query_then_fetch"}, body=search_data)
            return response
        except Exception as e:
            log.error(f"Sparse 검색 중 오류 발생 (인덱스: {index_name}): {e}")
            raise

    def execute_hybrid_search_with_pipeline(self, index_name: str, pipeline_name: str,
                                            query_vector: list, dense_field: str, k_dense: int,
                                            tokenized_query: str, sparse_field: str,
                                            size: int, source_excludes: list = None) -> dict:
        """
        Hybrid 검색을 검색 파이프라인을 사용하여 수행합니다.

        Args:
            index_name (str): 검색할 인덱스 이름입니다.
            pipeline_name (str): 사용할 검색 파이프라인 이름입니다.
            query_vector (list): Dense 검색을 위한 쿼리 임베딩 벡터입니다.
            dense_field (str): Dense 벡터 필드 이름입니다.
            k_dense (int): Dense 검색 (KNN)의 k 값입니다.
            tokenized_query (str): Sparse 검색을 위한 토큰화된 쿼리입니다.
            sparse_field (str): Sparse 벡터/토큰 필드 이름입니다.
            size (int): 반환할 결과의 최대 개수입니다.
            source_excludes (list, optional): 결과의 `_source` 필드에서 제외할 필드 목록입니다.

        Returns:
            dict: OpenSearch 검색 결과입니다.
        """
        log.info(f"Hybrid 검색 (파이프라인: {pipeline_name}) 실행: 인덱스='{index_name}', size={size}")
        search_data = {
            "size": size,
            "_source": {"excludes": source_excludes or []},
            "query": {
                "hybrid": {
                    "queries": [
                        {
                            "knn": {
                                dense_field: {
                                    "vector": query_vector,
                                    "k": k_dense
                                }
                            }
                        },
                        {
                            "match": {
                                sparse_field: tokenized_query
                            }
                        }
                    ]
                }
            }
        }
        try:
            response = self.client.transport.perform_request(
                method="POST", # _search 엔드포인트는 POST도 일반적으로 사용됩니다. GET도 가능.
                url=f"/{index_name}/_search?search_pipeline={pipeline_name}",
                body=search_data
            )
            return response
        except Exception as e:
            log.error(f"Hybrid 검색 (파이프라인: {pipeline_name}) 중 오류 발생 (인덱스: {index_name}): {e}")
            raise
