# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 한반도 좌표나 사각형 영역을 행정구역(시·도·시군구 등)으로 변환하고 GeoJSON으로 생성·시각화하는 도구입니다.
- **기술**: Python, Shapely/GeoPandas 기반 공간 처리, STRtree 공간 인덱스, GeoJSON 입출력.
- **특징**: 대량 사각형 변환 및 대표 텍스트 생성(성능 최적화된 rect2region_fast_v2), 섬 지역 자동 감지 및 행정구역 경계 조회, 변환 결과의 GeoJSON 생성 및 일괄 처리 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 → 전처리 → Kafka/Spark 스트리밍 → OpenSearch 업로드까지의 컨테이너 기반 E2E 파이프라인입니다.
- **기술**: Docker/Docker Compose, Apache Kafka(kRaft), Spark Structured Streaming, FastAPI, Nginx, OpenSearch, Selenium, Kiwipiepy.
- **특징**: 컨테이너화된 스트리밍 아키텍처와 네트워크 분리 구성, 실시간 전처리(문장 분리·오탈자 수정·불용어 처리) 및 Opensearch 연동, 사용자용 검색 UI와 연계된 데이터 흐름.

## B_project
- **설명**: 알고리즘 문제 풀이(코딩 테스트)용 라이브러리와 관련 도구·문서를 모아둔 프로젝트입니다.
- **기술**: Python(알고리즘 모듈, Jupyter Notebook), 자료구조·그래프·트리·문자열 알고리즘 구현, 운영/배포 가이드를 위한 FastAPI·DB 관련 문서.
- **특징**: boj_bible(기본/그래프/트리/고급 알고리즘 모듈), CT 자동화 및 LLM 연동 유틸(기본 모델 파라미터 변경 안내), kakao_history 노트북 및 배포·운영 가이드(special_prompt.md) 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 298fbab971a41696e2daddda34ca47c8883c4ff4 -->
