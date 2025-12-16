# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 단일 좌표를 대한민국(남한/북한) 행정구역으로 빠르게 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/GeoPandas 기반 공간처리, STRtree 공간 인덱스, GeoJSON
- **특징**: 고성능 rect2region_fast_v2를 통한 영역→행정구역 변환 및 대량 처리(convert_many), 섬 자동 감지·대표 텍스트 규칙, 경계 조회 및 GeoJSON 생성/시각화

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집해 문장 전처리 후 Kafka/Spark/Opensearch로 스트리밍 저장·검색하는 컨테이너화된 E2E 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI + Nginx, Kiwipiepy, Selenium(스크립트 수집)
- **특징**: Streaming 기반 전체 파이프라인(파일 감시 → Kafka → Spark 처리 → Opensearch 저장), 마이크로서비스 도커 네트워크 구성 및 Nginx 라우팅, 한국어 전처리 최적화(Kiwi + pandas_udf)

## B_project
- **설명**: 알고리즘 연습과 코딩 테스트 자동화를 위한 라이브러리·노트북·운영 가이드 모음입니다.
- **기술**: Python, Jupyter Notebook, (문서화로 FastAPI/Async, PostgreSQL/Redis 등 운영 스택 기술 포함)
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 제공, CT 자동화 도구 및 예제 노트북(B_project/CT/kakao_history.ipynb), 운영·개발 가이드(special_prompt.md) 및 LLM 유틸 변경 안내
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: ddb9290831594d490a4b22bb94ede5d83624273a -->
