# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 단일 좌표를 한국 행정구역(시/도/시군구 등)으로 빠르게 변환하고 GeoJSON으로 생성/시각화합니다.
- **기술**: Python, Shapely/GeoPandas 기반 공간처리, STRtree 공간 인덱스, GeoJSON 입출력.
- **특징**: 사각형→행정구역(대표/상세) 변환, 섬 자동 감지 및 방향 기반 대표표현, 경계 조회·GeoJSON 생성·일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 후 문장 전처리하여 Kafka→Spark→Opensearch로 업로드하는 Docker화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Kiwipiepy.
- **특징**: 전체 스트리밍 아키텍처(다중 컨테이너/네트워크), 한국어 전처리(pandas_udf로 Kiwi 적용), Kafka 토픽·OpenSearch 연동 및 웹 검색 인터페이스.

## B_project
- **설명**: 알고리즘 학습 및 코딩테스트 자동화용 리포지토리(문제 풀이 라이브러리·유틸).
- **기술**: Python 기반 자료구조·그래프·트리·문자열 알고리즘 모듈, Jupyter 노트북, 관련 운영 가이드 문서.
- **특징**: boj_bible 알고리즘 모듈 세트, CT 자동화 도구 및 LLM 유틸(기본 모델 변경 안내 포함), kakao_history 문제 풀이 노트북 및 개발 가이드.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: e8bec32c75ddd4ed1edf98b2107fd33c173fda8a -->
