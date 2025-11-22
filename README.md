# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 한반도(남/북) 행정구역으로 변환해 대표 텍스트·상세 정보·GeoJSON을 생성하는 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 색인, GeoJSON, 관련 데이터(대한민국/북한 GeoJSON).
- **특징**: 사각형→행정구역(대·시·군) 고속 변환(rect2region_fast_v2), 섬 자동 감지 및 방향 기반 대표 표현, 경계 조회·GeoJSON 생성·JSON 일괄 변환 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 수집 후 전처리하여 Kafka·Opensearch로 스트리밍 업로드하는 E2E Docker 기반 파이프라인입니다.
- **기술**: Docker-compose, Apache Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리), Selenium(수집 보조).
- **특징**: 마운트 폴더 감시→Spark readStream으로 Kafka 토픽 생성 및 가공, Kiwipiepy를 pandas_udf로 적용한 문장 전처리·오탈자 수정, Opensearch 색인 및 웹 검색 인터페이스 연동.

## B_project
- **설명**: 알고리즘/코딩 테스트 풀이용 라이브러리 및 관련 도구·문서 모음입니다.
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열·고급 알고리즘), Jupyter 노트북, FastAPI/Async 구성 문서(운영 가이드).
- **특징**: boj_bible(자료구조·알고리즘 구현) 제공, CT 자동화·LLM 연동 유틸(기본 모델 변경 안내 포함) 및 문제 풀이 샘플 노트북, AI 포털 운영·배포 가이드 문서 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 9c04953be1aaad50f16eaa0850dc19abcffc98c2 -->
