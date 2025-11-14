# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남/북한 포함) 행정구역으로 변환하고 GeoJSON으로 생성·시각화하는 도구입니다.  
- **기술**: Python, shapely/GeoPandas, STRtree 기반 Spatial Index, GeoJSON 출력.  
- **특징**: 사각형→행정구역 변환(전/부분 포함 판정 및 방향 표현), 섬 자동 감지(섬 표기 규칙), 대량 JSON 일괄 변환 및 경계 조회/GeoJSON 생성.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·Kafka·Opensearch 업로드까지 스트리밍 기반 E2E 파이프라인을 Docker 컨테이너로 구성한 프로젝트입니다.  
- **기술**: Docker Compose, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy.  
- **특징**: Spark readStream → Kafka 토픽 처리 → OpenSearch 적재 파이프라인, 컨테이너 기반 네트워크 구성(서비스 분리), 한국어 전처리(Kiwi)·pandas_udf 활용한 고속 처리.

## B_project
- **설명**: 알고리즘 문제 풀이(백준)용 라이브러리와 코딩 테스트 자동화·기록 도구를 모아둔 프로젝트입니다.  
- **기술**: Python 중심(자료구조·그래프·트리·문자열·고급 알고리즘), Jupyter 노트북, FastAPI/DB/Redis 관련 운영 가이드 문서 포함.  
- **특징**: boj_bible(기초~고급 알고리즘 모듈) 제공, CT 자동화 도구 및 LLM 호출 유틸(기본 모델 gpt-5-nano로 변경 안내), 문제 풀이 노트북·운영·배포 가이드 문서 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: f4654caee73e6cb704a7308756cd545447e2c153 -->
