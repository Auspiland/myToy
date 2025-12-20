# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 단일 좌표를 대한민국(남한/북한) 행정구역으로 매핑하고 GeoJSON으로 생성/시각화하는 GIS 변환 도구입니다.
- **기술**: Python, shapely/STRtree 기반 공간색인, GeoJSON, pandas, GitHub 연동 스크립트
- **특징**: 고성능 사각형→행정구역 변환(대량 처리 지원), 섬 자동 감지·대표 표현 규칙(면적 기반), 행정구역 경계 조회 및 GeoJSON 생성/시각화

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·OpenSearch 업로드까지 Docker 기반 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy
- **특징**: 실시간 스트리밍 ETL(파일 모니터링→Kafka→처리→인덱싱), Spark 기반 텍스트 전처리(병렬 pandas_udf 활용), 검색용 OpenSearch 인덱싱 및 웹 UI 연동

## B_project
- **설명**: 알고리즘 연습·코딩테스트 지원 라이브러리와 자동화 도구, 관련 노트북 및 운영 가이드 모음입니다.
- **기술**: Python(알고리즘 구현·유틸), FastAPI/Async DB 지침(문서), Jupyter 노트북
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT 자동화 도구 및 LLM 호출 유틸(기본 모델 변경 안내), 문제 풀이 노트북 및 운영·배포 가이드 문서 포함
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

<!-- LAST_PROCESSED_SHA: 1fe6616cecf8ab9cf7d86b573e0c422e6ed127bc -->
