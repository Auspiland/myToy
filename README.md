# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 단일 좌표를 한국 행정구역(시/도/시군구 등)으로 변환하고 경계·GeoJSON을 생성하는 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON/GeoPandas, 경계 데이터(국/도/리 수준).
- **특징**: 고성능 Rect→Region 변환(rect2region_fast_v2), 좌표→행정구역 매핑 및 섬 자동 감지, GeoJSON 생성·경계 조회·대량 JSON 변환 지원.

## Mini-Pipeline
- **설명**: YouTube URL을 입력으로 문장 전처리 후 Kafka와 OpenSearch로 업로드하는 컨테이너화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker(복수 compose 네트워크), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리).
- **특징**: 실시간 파일 감시→Spark로 Kafka 토픽 생성 및 변환, Kiwipiepy 기반 문장 분리·오탈자 보정·불용어 처리, OpenSearch 인덱싱 및 웹 검색 인터페이스.

## B_project
- **설명**: 알고리즘 풀이·코딩 테스트 지원 라이브러리 및 관련 도구 모음입니다.
- **기술**: Python, Jupyter 노트북, (FastAPI/LLM 헬퍼 등 프로젝트 문서 포함).
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT 자동화·LLM 호출 유틸(기본 모델 파라미터 변경 사항 포함), kakao_history 문제 풀이 노트북 및 개발·운영 가이드 문서.
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

<!-- LAST_PROCESSED_SHA: e59a7f56c374424511c50e38dec113d9c8e216b9 -->
