# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역 명칭으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, GeoJSON, Shapely/STRtree 기반 공간 인덱싱, geopandas(데이터 처리) 및 자체 모듈(Rect2Region).
- **특징**: 사각형→행정구역 변환(대규모 배치 지원), 좌표→행정구역 변환 및 섬 자동 감지, 결과 GeoJSON 생성 및 경계/중심점 조회 기능.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 → 문장 전처리 → Kafka/Opensearch에 업로드되는 Docker 기반 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium/Kiwipiepy(전처리).
- **특징**: 컨테이너별 네트워크 구성으로 서비스 분리(Streaming 모드), Spark ↔ Kafka ↔ OpenSearch 연계 파이프라인, Kiwipiepy 기반 한국어 전처리(udf/pandas_udf) 및 배치/스트리밍 처리.

## B_project
- **설명**: 알고리즘/코딩 테스트 풀이 및 관련 유틸리티를 모아 둔 프로젝트입니다.
- **기술**: Python 중심(라이브러리/노트북), Jupyter 노트북, (문서용) FastAPI·Async·Postgres·Redis 스택 가이드 포함.
- **특징**: boj_bible(자료구조·알고리즘 모듈) 구성, CT 자동화/기록 도구와 예제 노트북(kakao_history), CT용 LLM 유틸(common_utils) 기본 모델 변경 알림(gpt-5 → gpt-5-nano).
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

<!-- LAST_PROCESSED_SHA: 42bcf7849ab8c154fa4adab3c2d314d7e46e4ebc -->
