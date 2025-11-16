# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남북 포함) 행정구역으로 빠르게 매핑하는 도구  
- **기술**: Python, shapely(STRtree) 기반 공간 인덱스, GeoJSON 데이터 처리  
- **특징**: 사각형/포인트→시·도·시군구 변환(rect2region_fast_v2), GeoJSON 생성·시각화·경계·중심 조회, 섬 자동 감지 및 JSON 일괄 변환

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·Opensearch 적재까지의 Docker/Spark 기반 스트리밍 E2E 파이프라인  
- **기술**: Docker, Spark(Structured Streaming), Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리)  
- **특징**: 마운트 폴더 기반 스트리밍 ingestion → Kafka 토픽으로 전달 → Spark로 전처리 후 Opensearch 적재, Kiwipiepy 기반 한국어 전처리·Pandas UDF 적용, 웹 검색용 FastAPI/Nginx 연동

## B_project
- **설명**: 알고리즘·코딩 테스트 풀이와 자동화 도구를 모아둔 파이썬 프로젝트 모음  
- **기술**: Python(자료구조·그래프·트리·문자열 알고리즘), Jupyter 노트북, LLM 연동 유틸리티  
- **특징**: boj_bible(기본/그래프/트리/문자열/고급 알고리즘 라이브러리), CT 자동화 및 LLM 관련 유틸(모델 기본값 변경 등), 예제 노트북 및 개발/운영 가이드 문서
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 8199434f1cb03d0ba097566a60060644b17da8b1 -->
