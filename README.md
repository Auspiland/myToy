# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 한반도(남한/북한)에서 주어진 좌표 또는 사각형 영역을 행정구역으로 변환하고 GeoJSON으로 생성·시각화하는 파이썬 유틸리티.
- **기술**: Python, GeoJSON, Shapely/STRtree 기반 공간 인덱싱, 공간 경계 데이터(GeoJSON) 처리.
- **특징**: 고성능 rect2region_fast_v2 변환(대량 처리 가능), 섬 자동 감지 및 대표 텍스트 규칙, 행정구역 경계 조회·GeoJSON 일괄 변환/생성.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출→문장 전처리→Kafka·Spark·Opensearch로 업로드하는 컨테이너형 실시간(Streaming) E2E 파이프라인.
- **기술**: Docker Compose, Apache Kafka(kRaft), Apache Spark Streaming, FastAPI, Opensearch, Nginx, Selenium, Kiwipiepy.
- **특징**: 컨테이너별 네트워크 분리 및 compose 구성, Spark 기반 스트리밍 전처리(kiwipiepy·pandas_udf), 검색 UI 연동을 위한 Opensearch 적재.

## B_project
- **설명**: 알고리즘 및 코딩 테스트 문제 풀이와 자동화 도구(라이브러리·노트북·유틸)를 모아둔 프로젝트 모음.
- **기술**: Python(알고리즘 구현·Jupyter 노트북), 자료구조·그래프·트리 알고리즘 모듈, 일부 FastAPI·LLM 유틸 포함.
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT 자동화 도구 및 노트북(kakao_history) 포함, LLM 관련 기본 모델 변경 공지 및 재사용 권장 가이드.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 898520efc0a43e574c5dbfce52375bfec16e4569 -->
