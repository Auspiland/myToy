# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 입력한 좌표나 사각형 영역을 한반도 행정구역(시/도/시군구 등)으로 변환하고 GeoJSON으로 출력·시각화합니다.
- **기술**: Python, Shapely(STRtree) 기반 공간 색인, GeoJSON, geopandas 등 공간처리 라이브러리.
- **특징**: 최적화된 rect2region_fast_v2로 고속 변환(대량 처리 가능), 섬 지역 자동 감지·대표 표현 규칙, 행정구역 경계 조회·GeoJSON 생성 및 일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·Spark를 거쳐 OpenSearch에 업로드하는 Docker 기반 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Apache Spark 스트리밍, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy.
- **특징**: 컨테이너화된 전체 아키텍처(웹→API→파이프라인), Spark 스트리밍으로 Kafka·OpenSearch 연동, 한국어 전처리(오탈자 수정·문장 분리 등) 및 검색 UI 연동.

## B_project
- **설명**: 알고리즘 문제 해결과 코딩 테스트 자동화·기록을 위한 라이브러리 및 도구 모음입니다.
- **기술**: Python 기반 알고리즘 모듈, FastAPI/Async PostgreSQL/Redis 등(운영·개발 가이드 문서 포함).
- **특징**: boj_bible(자료구조·그래프·문자열·고급 알고리즘), CT 자동화와 LLM 유틸(기본 모델 변경 알림), 문제 풀이 노트북 및 개발·배포 가이드 문서.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 788db3516125335dd3ba24f2363fdd19b7fbec72 -->
