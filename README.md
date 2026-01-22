# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국 행정구역(시/도/군 등)으로 변환하고 GeoJSON으로 출력·시각화하는 도구입니다.
- **기술**: Python, shapely/STRtree(공간 인덱스), geopandas/GeoJSON, 경계 데이터(국·행정구역), 일부 LLM 기반 지명 처리
- **특징**: 사각형→행정구역(대표/상세) 변환, 섬 자동 감지(임계치 기반) 및 경계 조회, GeoJSON 생성·일괄 변환 지원

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka/Opensearch 업로드까지 Docker 기반으로 구성된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka (kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy
- **특징**: Spark→Kafka→Opensearch의 스트리밍 ETL 파이프라인, Kiwipiepy 기반 텍스트 전처리(pandas_udf 최적화), 멀티컨테이너 네트워크 및 웹 검색 인터페이스

## B_project
- **설명**: 알고리즘 연습·코딩테스트용 유틸과 자동화 도구들을 모아둔 프로젝트(라이브러리·노트북·운영 가이드 포함).
- **기술**: Python 기반 알고리즘 모듈(그래프·트리·문자열·고급 알고리즘), FastAPI/비동기 설계 문서 및 LLM 호출 유틸
- **특징**: boj_bible(자료구조·알고리즘) 모듈, CT 자동화·기록 도구 및 LLM 헬퍼(기본 모델이 gpt-5 → gpt-5-nano로 변경됨), 문제 풀이 노트북·개발·배포 가이드 포함
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

<!-- LAST_PROCESSED_SHA: c1c679c72805a734e88c1cb0d9d5e60c6bfec101 -->
