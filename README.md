# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 매핑하고 GeoJSON으로 시각화/배포하는 도구.
- **기술**: Python, Shapely/GeoPandas 기반 공간 처리, STRtree 공간 인덱스, GeoJSON 입출력.
- **특징**: 사각형→행정구역(대표·상세) 변환 및 대량 처리, 섬 자동 감지·방향 기반 대표문구 생성, 행정구역 경계 조회·GeoJSON 생성/배포 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·OpenSearch 업로드까지의 스트리밍 E2E 파이프라인.
- **기술**: Docker(Compose), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Selenium, Kiwipiepy.
- **특징**: Spark 기반 스트리밍 ingest→Kafka→OpenSearch 파이프라인, Kiwipiepy+룰베이스 전처리(오탈자·문장분리), 컨테이너화된 서비스 구성 및 검색 UI 연동.

## B_project
- **설명**: 알고리즘 학습·코딩테스트 풀이와 자동화 도구들을 모아둔 프로젝트 집합.
- **기술**: Python 중심(알고리즘 라이브러리, Jupyter 노트북), 테스트 자동화 스크립트, 보조 유틸리티.
- **특징**: boj_bible(자료구조·알고리즘) 모듈, CT 자동화·기록 도구 및 문제 풀이 노트북, LLM 응답 유틸(기본 모델 변경 등) 및 개발 가이드 문서 지원.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 98e0b66f5801d82361faa2b9bf175a3607951fd3 -->
