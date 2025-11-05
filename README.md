# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 단일 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구  
- **기술**: Python, Shapely/STRtree, GeoJSON, GeoPandas, LLM(지명 번역), GitHub 자동화  
- **특징**: 사각형→행정구역 변환 및 대량 처리(성능 최적화), 섬 자동 감지/방향 기반 대표 텍스트 생성, 행정구역 경계 조회·GeoJSON 생성·일괄 JSON 변환

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트를 추출해 문장 전처리하고 Kafka/Opensearch로 업로드하는 스트리밍 E2E 파이프라인  
- **기술**: Docker(다중 컨테이너), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy  
- **특징**: 컨테이너 기반 네트워크 아키텍처(서비스 분리), Spark로 파일→Kafka→Opensearch 스트리밍 파이프라인 구현, 한국어 전처리(오탈자·문장분리·불용어) 및 검색 인터페이스

## B_project
- **설명**: 알고리즘 문제 풀이와 코딩 테스트 자동화/기록을 위한 툴셋  
- **기술**: Python 기반 라이브러리 및 스크립트, LLM 연동 유틸리티  
- **특징**: boj_bible(기본 자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT 자동화 도구(기록·자동 풀이 보조), LLM 관련 유틸(기본 모델 파라미터 변경·스트리밍 지원)
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 8760661ef87522ed9f96c1633b8d58409b1d7774 -->
