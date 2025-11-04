# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 한반도(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화합니다.
- **기술**: Python, Shapely/STRtree(Spatial Index), GeoJSON/GeoPandas, GitHub 연동.
- **특징**: 사각형→행정구역 변환(광역/기초단위), 섬 자동 감지 및 대표 표기 규칙, 경계 조회·GeoJSON 생성 및 일괄 변환.

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트 추출 후 문장 전처리하여 Kafka와 OpenSearch로 업로드하는 컨테이너화된 스트리밍 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy, Selenium.
- **특징**: 컨테이너 기반 E2E 스트리밍 처리, Spark→Kafka→OpenSearch 연동, 한국어 전처리(오탈자 수정·문장 분리·불용어 처리) 및 검색 UI 연동.

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트 자동화·기록을 위한 도구 모음(백준용 라이브러리 포함).
- **기술**: Python, 자료구조·그래프·트리·문자열·고급 알고리즘 모듈, LLM 유틸리티.
- **특징**: boj_bible(기초·심화 알고리즘 모듈) 제공, CT 자동화 도구 및 기록 기능, LLM 관련 기본 모델 파라미터(gpt-5 → gpt-5-nano) 변경 알림.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 0902ae8c3f6d396d7cc9b82227bde47b41f3b6dd -->
