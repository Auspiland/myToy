# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 단일 좌표를 대한민국(남한/북한) 행정구역으로 매핑하고 GeoJSON으로 출력/시각화하는 도구입니다.
- **기술**: Python, Shapely/STRtree(공간인덱스), GeoJSON/GeoPandas, 기타 지오메트리 유틸리티.
- **특징**: 고성능 rect2region_fast_v2를 통한 대량 변환(배치/스트리밍), 섬 자동 감지 및 면적/방향 기반 대표 표현 생성, 행정구역 경계 조회 및 GeoJSON 파일 생성/일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 후 문장 전처리하여 Kafka → Spark → OpenSearch에 적재하는 Docker 기반 E2E 스트리밍 파이프라인입니다.
- **기술**: Docker Compose, Kafka(kRaft), Apache Spark(Streaming), OpenSearch, FastAPI, Nginx, Kiwipiepy(한국어 전처리).
- **특징**: 컨테이너 단위 네트워크 구성으로 서비스 분리·연동, Spark로 스트리밍 전처리 및 Opensearch 색인화, Kiwipiepy+pandas_udf 기반의 고속 한국어 전처리 파이프라인.

## B_project
- **설명**: 알고리즘·코딩 테스트 풀이 라이브러리 및 코딩 테스트 자동화/도구 모음입니다.
- **기술**: Python, Jupyter Notebook, 알고리즘 자료구조 구현(파이썬), (LLM 연동 유틸 포함).
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT 자동화용 유틸과 예제 노트북(kakao_history), LLM 호출 유틸 및 AI 포털 운영 가이드 문서 포함.
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
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 903e2e2aec8047dd84a7ac1bc9d830bb555e1862 -->
