# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 매핑하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 인덱스, GeoJSON, GeoPandas, 경계 데이터(GeoJSON).
- **특징**: 고성능 rect→region 변환(rect2region_fast_v2), 좌표→행정구역 변환 및 행정경계 조회, GeoJSON 생성·배치 변환 및 섬 자동 감지(방향/면적 기반 대표 표현).

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트를 추출해 문장 전처리 후 Kafka와 OpenSearch로 스트리밍 업로드하는 E2E 파이프라인입니다.
- **기술**: Docker(Compose), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy.
- **특징**: Spark readStream 기반 파일→Kafka 흐름 및 스트리밍 처리(전처리: Kiwipiepy·룰베이스), Kafka 토픽 연동 및 OpenSearch 인덱싱, 컨테이너 네트워크 구성으로 서비스 연동(웹 검색/서비스 노출).

## B_project
- **설명**: 알고리즘 학습·코딩테스트 지원용 라이브러리와 자동화 도구 모음입니다.
- **기술**: Python(모듈형 알고리즘 라이브러리), Jupyter 노트북, FastAPI/Async 관련 가이드 문서(운영·배포 참고).
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT 자동화 도구(LLM 호출 유틸 포함—기본 모델 변경 안내), 예제 노트북 및 운영·배포 가이드 문서 제공.
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

<!-- LAST_PROCESSED_SHA: 985b0faf640a8440cb72fac62ecf35beafcdb63d -->
