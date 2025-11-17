# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 단일 좌표를 한국 행정구역(광역/시·군·구 등)으로 빠르게 변환하고 시각화하는 도구입니다.
- **기술**: Python, shapely/STRtree 기반 공간 인덱싱, GeoJSON, geopandas 등 지리공간 라이브러리.
- **특징**: 사각형→행정구역/좌표→행정구역 변환, 섬 자동 감지 및 대표 텍스트 생성, 경계 조회·GeoJSON 생성 및 대량 변환(고성능 처리).

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 후 문장 전처리를 거쳐 Kafka와 OpenSearch로 업로드하는 컨테이너형 스트리밍 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy.
- **특징**: 컨테이너 기반 E2E 스트리밍 아키텍처, Spark→Kafka→OpenSearch 연계 파이프라인, 한국어 전처리(Kiwipiepy·규칙기반) 및 검색 인터페이스 제공.

## B_project
- **설명**: 알고리즘 학습 및 코딩테스트 도구 모음(라이브러리·연습 코드·노트북 포함)입니다.
- **기술**: Python, Jupyter Notebook, 알고리즘/자료구조 구현(스택·그래프·세그먼트트리 등).
- **특징**: boj_bible(기초·그래프·트리·문자열·고급 알고리즘) 라이브러리, CT 자동화·기록 도구 및 kakao_history 문제 풀이 노트북, LLM 관련 기본 모델이 gpt-5 → gpt-5-nano로 변경된 안내 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: f39af88983ef7a218cc659b51d3bddae24d63c42 -->
