# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역(시/도 등)으로 매핑하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, geopandas/shapely(STRtree), GeoJSON, 공간 인덱싱 및 일부 LLM 기반 지명 번역.
- **특징**: 사각형/포인트→행정구역 변환(대량 처리 최적화), 섬 자동 감지 및 대표 표현 생성, 행정구역 경계 조회·GeoJSON 생성·시각화.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 추출해 문장 전처리 후 Kafka→Spark→Opensearch로 스트리밍 인덱싱까지 처리하는 E2E 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy, Selenium(스크래핑).
- **특징**: 컨테이너 기반의 실시간 스트리밍 아키텍처, Spark↔Kafka↔Opensearch 연동 및 형태소 기반 전처리(병렬/Streaming), 웹 검색 인터페이스 제공.

## B_project
- **설명**: 알고리즘 학습·코딩 테스트용 라이브러리와 자동화 도구(문제 풀이, 유틸, 문서)를 모아둔 프로젝트입니다.
- **기술**: Python(알고리즘 모듈·Jupyter 노트북), FastAPI/비동기 DB 관련 문서, LLM 호출 유틸리티 포함.
- **특징**: boj_bible(자료구조·알고리즘 구현 모음), CT(코딩 테스트) 자동화 도구 및 예제, LLM 헬퍼 함수 변경 및 운영·배포 가이드 문서 제공.
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

<!-- LAST_PROCESSED_SHA: 0147b524f0447a689a4b1c842ae623a6ee7dff49 -->
