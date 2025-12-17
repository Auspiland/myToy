# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국/북한 행정구역(광역/시군구 등)으로 변환하고 경계/GeoJSON을 생성하는 도구입니다.  
- **기술**: Python, Shapely/GeoPandas, STRtree(공간 인덱스), GeoJSON 처리 및 파일 I/O.  
- **특징**: 사각형/점 → 행정구역 변환(대표 텍스트/상세), 섬 자동 감지 및 방향 기반 대표 표현 규칙, 행정구역 경계 조회·GeoJSON 생성 및 대량 JSON 변환 지원.

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트를 추출해 전처리하고 Kafka/Spark를 거쳐 OpenSearch에 색인하는 컨테이너화된 스트리밍 파이프라인입니다.  
- **기술**: Docker / docker-compose, Apache Kafka(kRaft), Spark Structured Streaming, OpenSearch, FastAPI, Nginx, Kiwipiepy(한국어 전처리).  
- **특징**: 스트리밍 기반 데이터 수집→전처리→Kafka 토픽·OpenSearch 색인, Spark에서의 pandas_udf/Kiwi 적용 및 장애/타이밍 고려한 처리(Timeout Trigger), 멀티컨테이너 네트워킹(웹 UI → FastAPI/Nginx → 검색).

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트 자동화·도구 모음(문제 풀이 라이브러리·자동화 스크립트 등) 프로젝트입니다.  
- **기술**: Python 중심(알고리즘·자료구조 구현), Jupyter 노트북, LLM 호출 유틸(프로젝트 내 GPT 래퍼).  
- **특징**: boj_bible(기본 자료구조·그래프·트리·문자열·고급 알고리즘) 라이브러리, CT 자동화 및 LLM 보조 함수(response_GPT 등) 업데이트·예제, 문제 풀이 노트북 및 운영·배포 가이드 문서 포함.
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

<!-- LAST_PROCESSED_SHA: 702a92ce28289c5ff56cbb766675611023b85947 -->
