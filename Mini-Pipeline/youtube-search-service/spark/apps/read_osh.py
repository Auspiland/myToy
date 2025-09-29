from opensearchpy import OpenSearch
from tools.print_smth import print_dict


# OpenSearch 클라이언트 설정
client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    use_ssl=False  # https가 아니면 False
)

# <<쿼리 생성>>
# 전체 문서를 반환하는 쿼리
{
  "query": {
    "match_all": {}  # 조건 없이 모든 문서를 반환
  }
}

# 분석기를 적용한 필드에 대해 자연어 유사도 검색 수행
{
  "query": {
    "match": {
      "title_name": "AI 시대"  # 분석기 사용됨 (형태소 단위 분해)
    }
  }
}

# 분석기 없이, 정확히 일치하는 값 검색 (keyword 필드에서 주로 사용)
{
  "query": {
    "term": {
      "language": "ko"  # 완전한 문자열 일치 검색
    }
  }
}

# 여러 조건을 조합한 검색 쿼리
{
  "query": {
    "bool": {
      "must": [  # AND 조건
        { "match": { "language": "ko" }},  # language가 ko
        { "range": { "published_at": { "gte": "2023-01-01" }}}  # 2023년 이후
      ],
      "must_not": [  # NOT 조건
        { "match": { "err_cd": "ERR001" }}  # err_cd가 ERR001인 건 제외
      ]
    }
  }
}

# 와일드카드를 사용한 부분 단어 검색 (*는 0개 이상의 문자)
{
  "query": {
    "wildcard": {
      "title_name.keyword": "*인공지능*"  # 인공지능이 포함된 모든 문자열 검색
    }
  }
}

# 접두어 기반 검색 (prefix)
{
  "query": {
    "prefix": {
      "video_id.keyword": "dQw"  # dQw로 시작하는 video_id 검색
    }
  }
}

# 날짜 범위 검색 쿼리
{
  "query": {
    "range": {
      "published_at": {
        "gte": "2023-01-01",  # 2023-01-01 이후
        "lte": "2023-12-31"   # 2023-12-31 이전
      }
    }
  }
}

# 특정 필드가 존재하는 문서만 반환
{
  "query": {
    "exists": {
      "field": "script"  # script 필드가 존재하는 문서만 검색
    }
  }
}

# 결과를 날짜 기준 내림차순 정렬하고, 10건만 가져오기
{
  "query": {
    "match_all": {}  # 전체 검색
  },
  "sort": [
    { "published_at": { "order": "desc" }}  # 날짜 기준 정렬
  ],
  "from": 0,  # 시작 인덱스
  "size": 10  # 최대 10개 문서
}

# 일부 필드만 반환하도록 제한
{
  "_source": ["title_name", "published_at"],  # 반환할 필드만 지정
  "query": {
    "match_all": {}
  }
}



def search_osh(query):
    # 검색
    response = client.search(index="script_index", body=query)

    for hit in response["hits"]["hits"]:
        print_dict(hit["_source"])



def explain_osh(query):
    doc_id = "SDZPKpgBLap-DocuAUBZ"

    explanation = client.explain(index="script_index", id=doc_id, body=query)
    print(explanation)
