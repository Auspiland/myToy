# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남·북) 행정구역으로 자동 변환해주는 도구  
- **기술**: Python, GeoPandas / Shapely(STRtree) 기반 공간색인, GeoJSON 입출력  
- **특징**: 사각형→행정구역(고속화된 rect2region_fast_v2), 좌표→행정구역 및 경계 조회, GeoJSON 생성·시각화 및 섬 지역 자동 감지

## Mini-Pipeline
- **설명**: YouTube URL → 문장 전처리 → Kafka/Opensearch 업로드까지의 Docker화된 스트리밍 E2E 파이프라인  
- **기술**: Docker Compose, Kafka(kRaft), Spark(Structured Streaming), OpenSearch, FastAPI + Nginx, Selenium/Kiwipiepy(전처리)  
- **특징**: 디렉토리 감시 기반 Spark 스트리밍 → Kafka 토픽 흐름 및 Opensearch 색인, Kiwipiepy 기반 한국어 전처리(udf), 멀티컨테이너 네트워크 구성 및 웹 검색 인터페이스

## B_project
- **설명**: 알고리즘 풀이·코딩 테스트 보조를 위한 라이브러리 및 도구 모음  
- **기술**: Python 기반 알고리즘 모듈 및 Jupyter 노트북(문제 풀이/시뮬레이션)  
- **특징**: boj_bible(기초 자료구조·그래프·트리·문자열·고급 알고리즘) 모듈화, CT 자동화 도구·노트북 포함, CT 관련 LLM 호출 유틸의 기본 모델이 gpt-5 → gpt-5-nano로 변경된 안내 문서 포함
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: c1b9cae90e67a6a86c28916d2baa9d039d4cc746 -->
