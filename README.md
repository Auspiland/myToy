# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 한국 행정구역(시/도/군/구/리 등)으로 매핑하고 GeoJSON으로 생성·시각화하는 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON/쉐이프파일 데이터, LLM(지명 번역) 및 GitHub 연동.
- **특징**: 사각형→행정구역 변환(rect2region_fast_v2), 좌표→행정구역 변환 및 경계 조회, GeoJSON 생성·일괄 변환 및 섬 자동 감지.

## Mini-Pipeline
- **설명**: YouTube 스크립트 수집 후 문장 전처리하여 Kafka → Spark → Opensearch로 업로드하는 컨테이너 기반 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Kafka(kRaft), Apache Spark Structured Streaming, FastAPI, Nginx, Opensearch, Selenium, Kiwipiepy.
- **특징**: Streaming 모드의 토픽 기반 처리(Kafka/Spark 연동), 한국어 전처리(F.pandas_udf + Kiwi) 및 Opensearch 색인, Nginx+FastAPI 기반 웹 조회 인터페이스.

## B_project
- **설명**: 알고리즘 학습·코딩테스트 대비용 라이브러리 및 자동화/기록 도구 모음입니다.
- **기술**: Python 기반 알고리즘 모듈 및 유틸리티, LLM 호출 유틸 통합.
- **특징**: boj_bible(자료구조/그래프/트리/문자열/고급 알고리즘) 모듈, CT 자동화/기록 도구, LLM 관련 유틸의 기본 모델이 gpt-5 → gpt-5-nano로 변경(명시적 지정 가능).
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 9a5f023fa5d2503af8ed99bd383ecc655d128b7f -->
