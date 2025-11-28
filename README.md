# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역명으로 변환하고 시각화하는 도구  
- **기술**: Python, Shapely/GeoPandas 기반 공간인덱스(STRtree), GeoJSON 입출력  
- **특징**: 사각형/포인트→행정구역 변환(대·시·군·읍·리 수준), 섬 자동 감지 및 행정경계 조회, GeoJSON 생성·일괄 JSON 변환

## Mini-Pipeline
- **설명**: YouTube URL을 입력받아 문장 전처리 후 Kafka와 OpenSearch로 업로드하는 도커화된 스트리밍 E2E 파이프라인  
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy  
- **특징**: Spark→Kafka→OpenSearch 흐름의 실시간 처리(WriteStream/ReadStream), 웹 인터페이스(Nginx+FastAPI) 연동, 한국어 전처리(Kiwi)용 pandas UDF 적용

## B_project
- **설명**: 알고리즘/코딩 테스트 풀이 및 관련 도구 모음 (문제풀이 라이브러리·자동화 도구 등)  
- **기술**: Python 기반 알고리즘 모듈, 노트북(.ipynb), FastAPI/DB/Redis 운영 가이드 문서 등  
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT 자동화 및 LLM 유틸(기본 모델 변경 등) 예제·노트북 포함
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 871473a5f74199aad51014da69bfc9707f3c124c -->
