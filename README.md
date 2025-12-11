# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표(또는 사각형 영역)를 한국 행정구역(시/도/군/구 등)으로 변환하고 GeoJSON 생성·시각화하는 도구.
- **기술**: Python, shapely/STRtree 기반 공간 인덱싱, GeoJSON, pyproj/판다스 등 공간처리 스택.
- **특징**: 사각형→행정구역 변환(대표 텍스트 옵션 포함), 좌표→행정구역 및 경계 조회·섬 자동 감지, 대량 JSON 일괄 변환 및 GeoJSON 출력/시각화.

## Mini-Pipeline
- **설명**: YouTube URL에서 스크립트 추출 후 문장 전처리하여 Kafka와 OpenSearch로 업로드하는 도커 기반 스트리밍 E2E 파이프라인.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Selenium, Kiwipiepy.
- **특징**: Streaming 모드의 Spark↔Kafka↔OpenSearch ETL 파이프라인, Kiwipiepy 기반 텍스트 전처리(오탈자 수정·문장 분리 등), 컨테이너별 네트워크 분리 및 운영 자동화 구성.

## B_project
- **설명**: 알고리즘·코딩 테스트 풀이용 라이브러리 및 관련 도구·문서 모음 프로젝트.
- **기술**: Python(자료구조·그래프·트리·문자열 알고리즘), Jupyter 노트북, FastAPI/Async 관련 운영 가이드, LLM 유틸리티.
- **특징**: boj_bible(기초∼고급 알고리즘 모듈), CT 자동화 및 문제 풀이 유틸리티(모델 기본값 변경 등), 노트북 예제 및 배포·운영 가이드(special_prompt.md).
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 31cdbf17a739666627c7b652bede7088f084703a -->
