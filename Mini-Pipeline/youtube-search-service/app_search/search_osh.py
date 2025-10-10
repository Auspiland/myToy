from opensearchpy import OpenSearch

# OpenSearch 클라이언트 생성
client = OpenSearch(
    hosts=[{"host": "host.docker.internal", "port": 9200}],
    http_auth=("admin", "admin"),
    use_ssl=False
)

# 검색 함수
def search_by_title(index: str, query: str):
    response = client.search(
        index=index,
        body={
            "query": {
                "match": {
                    "title_name": query
                }
            }
        }
    )
    return [{"title": hit["_source"]["title_name"], "script": hit["_source"]["script"]} for hit in response["hits"]["hits"]]

