# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->
## [geo_map]
- **설명**: 사각형 영역이나 단일 좌표를 대한민국(남북) 행정구역(시/도/구 등)으로 변환하고 GeoJSON으로 시각화하는 GIS 유틸리티.
- **기술**: Python, shapely/STRtree 기반 공간 인덱싱, GeoJSON/geo파이프라인, geopandas 등 GIS 도구.
- **특징**: 고성능 rect2region_fast_v2(대량 처리 최적화), 섬 자동 감지 및 대표표현 규칙, 경계 조회·GeoJSON 생성·JSON 일괄 변환 지원.

## [Mini-Pipeline]
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka→Spark→OpenSearch 업로드까지의 컨테이너 기반 스트리밍 E2E 파이프라인.
- **기술**: Docker Compose, Apache Spark Streaming, Kafka, OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy.
- **특징**: 컨테이너별 네트워크 설계(Shared-net), 스트리밍 파일 감시→Kafka 토픽 처리→OpenSearch 적재 플로우, 한국어 전처리(키위·pandas_udf) 및 웹 검색 인터페이스.

## [B_project]
- **설명**: 알고리즘 문제 풀이 및 코딩 테스트 지원 라이브러리·도구 모음(예제·노트북 포함).
- **기술**: Python 중심(모듈·노트북), 알고리즘 구현(그래프/트리/문자열/고급), LLM 연동 유틸리티.
- **특징**: BOJ용 알고리즘 모듈(자료구조·그래프·트리 등), CT 자동화/기록 도구 및 예제 노트북, LLM 관련 유틸(기본 모델 gpt-5-nano로 변경 안내 포함).
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 524c4d84216dd561983bc9798d273cd6a84ac2cd -->
