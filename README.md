# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->

## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 파이썬 기반 도구  
- **기술**: Python, Shapely/STRtree 기반 공간 인덱스, GeoJSON, 행정구역 GeoJSON 데이터  
- **특징**: 사각형→행정구역 변환(대표표현/상세), 좌표→행정구역 변환 및 경계 조회, 섬 자동 감지·GeoJSON 생성 및 시각화

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·Kafka 전송·Opensearch 인덱싱까지의 스트리밍 기반 E2E 파이프라인  
- **기술**: Docker(Compose), Apache Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy(형태소), Selenium(스크립트 수집)  
- **특징**: 컨테이너화된 스트리밍 파이프라인(Spark↔Kafka↔Opensearch), 한국어 전처리(키위+규칙) 및 pandas_udf 적용, 웹 검색 인터페이스 연동

## B_project
- **설명**: 알고리즘 문제 풀이와 코딩 테스트 자동화·보조 도구 모음 저장소  
- **기술**: Python 중심(문제 풀이 라이브러리·노트북·FastAPI 등 문서·도구 혼합)  
- **특징**: boj_bible(자료구조·알고리즘 모듈) 컬렉션, CT 자동화/LLM 유틸(기본 모델 변경 알림 포함), 문제 풀이 노트북 및 운영·개발 가이드 문서 제공

<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: d36b11ab4247a0c5ad317019770bf498d367c58e -->
