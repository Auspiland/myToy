# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한 포함)의 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, geopandas/shapely, STRtree 공간 인덱스, GeoJSON, LLM(지명 번역) 및 GitHub 연동.
- **특징**: 사각형/좌표 → 행정구역 변환(rect2region_fast_v2) 및 대량 처리, 섬 자동 감지·대표 텍스트 생성, 행정구역 경계 조회·GeoJSON 생성 기능.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리(한국어) → Kafka/Spark 스트리밍 → Opensearch 업로드까지의 E2E 파이프라인입니다.
- **기술**: Docker(Compose), Apache Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리).
- **특징**: 컨테이너화된 스트리밍 아키텍처, Spark에서 Kafka/Opensearch 연동 및 F.pandas_udf 기반 전처리, 웹 인터페이스(검색·조회) 제공.

## B_project
- **설명**: 알고리즘 문제 풀이와 코딩 테스트 자동화·도구 모음을 담은 프로젝트입니다.
- **기술**: Python 기반 알고리즘 라이브러리/유틸, Jupyter 노트북, LLM 연동 유틸(FAST API · 비동기 DB 관련 가이드는 문서화).
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT 자동화(LLM 기본 모델 변경·스트리밍 지원 포함), 문제 풀이 노트북 및 운영·배포 가이드(special_prompt.md).
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: d90775e2ccd6fb17c48d3dc2133d2f6b78815fcb -->
