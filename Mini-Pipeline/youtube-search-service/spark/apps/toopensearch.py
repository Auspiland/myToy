

# OSH_NODES = "http://localhost:9200"
# OSH_NODES = "opensearch-node1:9200"


def write_opensearch(data, checkpoint_path="/tmp/checkpoint_opensearch", index_name="script_index"):
    opensearch_conf = {
        "opensearch.nodes": "host.docker.internal",
        "opensearch.port": "9200",
        "opensearch.ssl": "false",                # TLS 비활성화 시 : HTTPS 대신 HTTP
        "opensearch.index.auto.create": "true",   # 인덱스 자동 생성 허용
        "opensearch.nodes.wan.only": "true"       # 호스트에서 외부 OpenSearch 접근 시 반드시 필요
    }

    query = data.writeStream \
        .format("opensearch") \
        .options(**opensearch_conf) \
        .option("checkpointLocation", checkpoint_path) \
        .outputMode("append") \
        .start(index_name)

    print(f"📡 Streaming to OpenSearch index '{index_name}' 시작됨")
    return query

