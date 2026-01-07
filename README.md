# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 경계·GeoJSON을 생성·시각화하는 지리정보 변환 도구입니다.  
- **기술**: Python, Shapely/GeoPandas, STRtree 공간 인덱스, GeoJSON 기반 데이터 (using_data), 성능 최적화된 rect2region_fast_v2 구현.  
- **특징**: 사각형→행정구역 변환(대량 처리 지원), 좌표→행정구역·경계 조회 및 중심점 반환, GeoJSON 생성·시각화(섬 자동 감지 포함).

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka 전송·Spark 처리·Opensearch 업로드·검색 UI 노출까지의 E2E 스트리밍 파이프라인입니다.  
- **기술**: Docker (multi-compose), Apache Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Selenium(스크립트 수집), Kiwipiepy 기반 텍스트 전처리.  
- **특징**: 컨테이너화된 스트리밍 파이프라인(파일 모니터→Kafka→Spark→Opensearch), 한국어 전처리(Kiwi, 규칙 기반 오탈자/문장 분리), 검색·웹 노출을 위한 Opensearch 연동.

## B_project
- **설명**: 알고리즘 문제 풀이·코딩 테스트 보조 라이브러리와 관련 도구들을 모아둔 프로젝트입니다.  
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열·고급 알고리즘), Jupyter 노트북 예제 및 FastAPI/LLM 연동 유틸(문서화).  
- **특징**: boj_bible(기본 자료구조·알고리즘 모듈) 제공, CT(코딩 테스트) 자동화·예제 함수들(노트북 포함), LLM 호출 유틸 기본 모델 변경 등 운영·개발 문서 포함.
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

<!-- LAST_PROCESSED_SHA: 73df18c39c5ca8bc8786462b05b2e8756c4f6667 -->
