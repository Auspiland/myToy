# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역 단위로 빠르게 변환하고 GeoJSON으로 출력하는 툴입니다.
- **기술**: Python 기반(Shapely STRtree 등 공간 색인), GeoJSON 중심의 경계 데이터 사용.
- **특징**: 고성능 rect→region 변환(rect2region_fast_v2), 섬 자동 감지 및 방향 기반 대표 표현, GeoJSON 생성·시각화·일괄 변환 기능.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집해 문장 전처리 후 Kafka/OpenSearch로 스트리밍 업로드하는 컨테이너화된 E2E 파이프라인입니다.
- **기술**: Docker Compose(다중 네트워크), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy, Selenium(수집 보조).
- **특징**: 실시간 스트리밍 파이프라인(파일→Spark→Kafka→OpenSearch), 한국어 전처리(korean tokenization + 룰베이스), 컨테이너별 네트워크·배포 구성 제공.

## B_project
- **설명**: 알고리즘 연습(BOJ)과 코딩 테스트 자동화·기록을 위한 도구 모음입니다.
- **기술**: Python 기반 알고리즘 라이브러리·노트북, FastAPI/비동기 유틸 문서(운영 가이드 포함), LLM 통합 유틸.
- **특징**: boj_bible(자료구조·그래프·트리·문자열 등) 모듈화, CT 자동화(LLM 호출 유틸 및 기본 모델 파라미터 변경 이력 포함), 문제 풀이 노트북 및 개발·배포 가이드 문서화.
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

<!-- LAST_PROCESSED_SHA: 95958c3d1a7ffdda541c4cb2ad1b4b6d339c91f1 -->
