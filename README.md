# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 단일 좌표를 받아 대한민국(남한/북한) 행정구역(시/도 등)으로 자동 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, geopandas/shapely, STRtree 공간 인덱스, GeoJSON, GitHub 자동 푸시 스크립트.
- **특징**: 사각형→행정구역 변환(대량 처리/성능 최적화), 좌표→행정구역 매핑 및 섬 자동 감지, GeoJSON 생성·조회·경계 정보 제공.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 → 문장 전처리 → Kafka/Spark 스트리밍 처리 → OpenSearch 업로드까지의 E2E 컨테이너화된 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy(한국어 전처리).
- **특징**: 스트리밍 기반 파일 감시 → Kafka 토픽 연동·가공 → OpenSearch 인덱싱, 웹 검색 인터페이스( FastAPI/Nginx ), 컨테이너 네트워크 분리로 구성 관리.

## B_project
- **설명**: 알고리즘/코딩 테스트 연습용 라이브러리 및 자동화 도구 모음(문제 풀이 유틸·노트북 포함)입니다.
- **기술**: Python(문제 풀이 스크립트, Jupyter), FastAPI/Async 도구(문서 참조), LLM 호출 유틸 등.
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT(코딩 테스트) 자동화 및 기록 도구, 추가된 kakao_history 노트북과 LLM 유틸 기본 모델(gpt-5 → gpt-5-nano) 변경 안내.
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

<!-- LAST_PROCESSED_SHA: 634ab4a801f721ae7256a99a0cf127416a28e724 -->
