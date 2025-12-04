# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 한반도(남한/북한) 내 좌표 또는 사각형 영역을 행정구역(시·도·시군구 등)으로 변환하고 GeoJSON으로 생성/시각화합니다.  
- **기술**: Python, Shapely/STRtree 공간 인덱스, GeoJSON, 지역 경계 GeoJSON 데이터.  
- **특징**: 사각형→행정구역 일괄 변환(고속화된 rect2region_fast_v2), 좌표→행정구역 변환 및 경계 조회, 섬 자동 감지·GeoJSON 생성.

## Mini-Pipeline
- **설명**: 유튜브 URL로부터 스크립트를 추출해 문장 전처리 후 Kafka→Spark→OpenSearch로 업로드하는 Docker 기반 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Kiwipiepy(한국어 전처리).  
- **특징**: 파일 모니터링 기반 스트리밍 파이프라인, 한국어 전처리(오탈자 수정·문장 분리) 및 검색 인덱싱, 멀티 컨테이너 네트워크 구성.

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트용 라이브러리·도구와 관련 문서·노트북 모음입니다.  
- **기술**: Python(알고리즘 모듈), Jupyter Notebook, (문서 참조용) FastAPI/Async 툴 체계.  
- **특징**: boj_bible(자료구조·그래프·트리·문자열 등) 모듈, CT 자동화·LLM 헬퍼(기본 모델 변경 안내 포함), 문제 풀이 노트북 및 운영/배포 가이드 문서.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 4ab7fecad4b6823653d30032c9680f86eac3a2e2 -->
