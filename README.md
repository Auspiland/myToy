# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 단일 좌표를 대한민국(남한/북한) 행정구역(시/도/시군구 단위)으로 빠르게 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/STRtree 공간 색인, GeoJSON, Pandas 등 지리공간 처리 스택.
- **특징**: 고성능 사각형→행정구역 변환(rect2region_fast_v2), 섬 지역 자동 감지 및 대표 문장 생성, 행정구역 경계 조회·GeoJSON 생성 및 일괄 변환 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·Kafka 전송·Spark 처리·Opensearch 색인까지 Docker 기반으로 구성된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Apache Spark(Structured Streaming), Kafka(kRaft), Opensearch, FastAPI, Nginx, Selenium, Kiwipiepy(한국어 전처리).
- **특징**: Spark readStream→Kafka 토픽 기반 파이프라인·Opensearch 색인, Kiwipiepy 기반 문장 전처리(pandas_udf 최적화), 컨테이너 간 네트워크 분리·운영(Shared-net 등).

## B_project
- **설명**: 알고리즘 학습·코딩테스트 문제 풀이용 라이브러리 및 자동화 도구를 모아둔 프로젝트입니다.
- **기술**: Python, Jupyter Notebook, 알고리즘 구현(그래프·트리·문자열 등), FastAPI/LLM 유틸(프로젝트 내 CT 도구 연계).
- **특징**: boj_bible 모듈(자료구조·그래프·트리·문자열·고급 알고리즘) 제공, CT 자동화·LLM 호출 유틸(기본 모델 변경 공지 포함), kakao_history 등 실전 풀이 노트북 예제 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: d048b5e2b37bf153975e42ba33da9c9cfdcff148 -->
