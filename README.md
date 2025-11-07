# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남/북) 행정구역으로 빠르게 매핑하는 도구입니다.  
- **기술**: Python, Shapely/GeoPandas 기반 공간 인덱스(STRtree), GeoJSON 입출력.  
- **특징**: 사각형→행정구역 고속 변환(대량 처리), 좌표 기반 영역/경계 조회 및 섬 자동 감지, GeoJSON 생성·시각화 및 JSON 일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리 후 Kafka·OpenSearch로 업로드하는 E2E 스트리밍 파이프라인입니다.  
- **기술**: Docker(다중 컨테이너), Apache Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy, Selenium.  
- **특징**: Spark 기반 스트리밍 파이프라인(Kafka↔OpenSearch) 구성, Kiwipiepy+룰 기반 한국어 전처리(pandas_udf 사용), docker-compose로 분리된 네트워크·서비스 운영.

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트 자동화·도구 모음 프로젝트입니다.  
- **기술**: Python 기반 알고리즘 라이브러리 및 자동화 스크립트, LLM 연동 유틸리티 포함.  
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, 코딩 테스트 자동화(CT) 도구, CT용 LLM 기본 모델이 gpt-5 → gpt-5-nano로 변경된 알림 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 61e5bc070619d8cd4758c214df0ed0a308f43a40 -->
