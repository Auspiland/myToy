#------------------------------------------------------------
# Custom OpenSearch 2.19.1 with analysis-nori (k-NN는 기본 포함)
#------------------------------------------------------------
    ARG OPENSEARCH_VERSION=2.19.1
    FROM opensearchproject/opensearch:${OPENSEARCH_VERSION}
    
    # 1) 플러그인 추가 설치는 root 권한 필요
    USER root
    
    # 2) Korean Nori tokenizer 플러그인만 설치
    RUN /usr/share/opensearch/bin/opensearch-plugin install --batch analysis-nori \
        && chown -R opensearch:opensearch /usr/share/opensearch
    
    # 3) 권한 복귀
    USER opensearch

# opensearch-knn-nori:2.19.1로 빌드