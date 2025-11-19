# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표(점) 또는 사각형 영역을 한국 행정구역(광역/시도/시군구 등)으로 변환해 대표 표현과 상세 포함 리스트를 반환합니다.
- **기술**: Python, GeoJSON 기반 경계 데이터, Shapely/STRtree 공간 인덱스, GitHub 연동
- **특징**: 사각형→행정구역 변환(대표문구/상세), 섬 자동 감지 및 경계 조회, GeoJSON 생성·대량 변환 지원

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리, Kafka·Opensearch에 업로드하는 Docker화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리)
- **특징**: 파일 감시→Spark→Kafka→Opensearch 스트리밍 처리, Kiwi 기반 문장 전처리(pandas_udf), 컨테이너별 네트워크 분리 및 웹 인터페이스 연동

## B_project
- **설명**: 알고리즘 풀이·코딩 테스트용 라이브러리와 자동화 도구 모음입니다.
- **기술**: Python, Jupyter Notebook, 알고리즘 모듈화(boj_bible), LLM 유틸리티 포함
- **특징**: 자료구조·그래프·문자열 등 알고리즘 모듈 제공, CT 자동화 도구 및 LLM 호출 유틸(기본 모델 변경 안내), kakao_history.ipynb·운영 가이드 문서 추가
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 2108f40ce5b8cfc1d74f298673d5442639ef82a0 -->
