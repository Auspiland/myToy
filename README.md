# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국/북한 행정구역으로 변환하고 GeoJSON으로 시각화하는 공간 변환 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간색인, GeoJSON, Pandas 등 (pip로 의존성 설치).
- **특징**: 빠른 Rect→Region 변환(rect2region_fast_v2), 좌표→행정구역 변환 및 경계 조회, 섬 자동 감지·GeoJSON 생성·배치 JSON 변환 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리, Kafka·Spark 스트리밍 파이프라인을 통해 OpenSearch에 업로드하는 E2E 도구입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy.
- **특징**: 컨테이너 기반 멀티네트워크 아키텍처, Spark→Kafka→OpenSearch 흐름으로 실시간 처리, Kiwipiepy 및 pandas_udf를 이용한 언어 전처리와 검색용 인덱싱.

## B_project
- **설명**: 알고리즘 문제 풀이용 라이브러리(boj_bible)와 코딩 테스트 자동화·기록 도구를 모아둔 프로젝트입니다.
- **기술**: Python, Jupyter Notebook, 알고리즘 유틸 모듈, FastAPI 관련 문서(운영 가이드), LLM 유틸리티.
- **특징**: 기본/그래프/트리/문자열/고급 알고리즘 모듈 제공, CT 자동화·LLM 헬퍼(response_GPT 계열) 포함(기본 모델이 gpt-5 → gpt-5-nano로 변경), kakao_history.ipynb·운영 가이드 문서 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: d181a7d6c013389c73312a204a71f4c0a812ca01 -->
