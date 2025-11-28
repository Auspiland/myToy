# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 빠르게 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 색인, GeoJSON, 주요 행정구역 데이터(GeoJSON).
- **특징**: 사각형→행정구역 변환(고성능 v2), 좌표→행정구역 매핑 및 섬 자동 감지, GeoJSON 생성·경계 조회·대량 변환 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 → 문장 전처리 → Kafka/Opensearch로 업로드하는 컨테이너화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Kafka(kRaft), Apache Spark(Structured Streaming), FastAPI, Nginx, Opensearch, Selenium, Kiwipiepy.
- **특징**: Spark 기반 스트리밍 ETL(파일 감시 → Kafka → Opensearch), 한국어 전처리(Kiwi + pandas_udf) 및 컨테이너 간 네트워크 분리·운영 구성.

## B_project
- **설명**: 알고리즘 문제 풀이·코딩 테스트용 라이브러리와 자동화 도구를 모아둔 프로젝트입니다.
- **기술**: Python 중심(알고리즘 모듈, Jupyter 노트북), FastAPI/DB/CI 가이드 문서 포함(운영 가이드용 문서).
- **특징**: boj_bible(자료구조·그래프·트리·문자열 등) 모듈, CT 자동화 도구 및 예제 노트북(kakao_history), LLM 관련 유틸 기본 모델 변경 안내(gpt-5 → gpt-5-nano).
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 9fa958a5f91aef3c03a9e503d464064a25c919ce -->
