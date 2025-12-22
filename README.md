# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남·북한 포함) 행정구역으로 빠르게 변환하고 GeoJSON으로 시각화하는 툴입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON, spatial data (using_data), GitHub 푸시 유틸리티.
- **특징**: 사각형→행정구역 변환(최적화된 rect2region_fast_v2), 섬 자동 감지 및 대표 표현 규칙, 행정구역 경계 조회·GeoJSON 생성·일괄 변환 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 수집 → 문장 전처리 → Kafka·Opensearch로 업로드되는 컨테이너화된 E2E 스트리밍 파이프라인입니다.
- **기술**: Docker(다중 compose), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium(스크립트 수집), Kiwipiepy(한국어 전처리).
- **특징**: 마운트 폴더 감시·Spark readStream 기반 ingest, Kiwipiepy + 룰베이스 전처리(pandas_udf 활용), Kafka 토픽·Opensearch 인덱싱 및 웹 검색 연동.

## B_project
- **설명**: 알고리즘 문제 풀이·코딩 테스트용 라이브러리와 자동화 도구를 모은 프로젝트입니다.
- **기술**: Python(알고리즘 모듈, Jupyter 노트북), FastAPI/운영 가이드 문서(특정 서브문서), LLM 호출 유틸리티 포함.
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈화, CT 자동화 및 LLM 유틸(기본 모델 변경 안내), kakao_history 노트북·운영·배포 가이드 문서 포함.
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

<!-- LAST_PROCESSED_SHA: 7040f9d031cbe252c4b29d3d4392817301c20be1 -->
