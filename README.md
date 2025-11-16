# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역 표현으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely/GeoPandas 기반 공간 처리, STRtree 공간 인덱스, GeoJSON 출력.  
- **특징**: 사각형→행정구역 변환(대량 처리 지원), 좌표→행정구역 변환 및 경계 조회, 섬 자동 감지·GeoJSON 생성 및 시각화.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 후 문장 전처리하여 Kafka·Opensearch로 업로드하는 컨테이너화된 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Selenium/Kiwipiepy(한국어 전처리).  
- **특징**: 전체 스트리밍 파이프라인(파일 감시→Kafka→가공→Opensearch), 컨테이너 네트워크 분리 및 로그/디버깅을 위한 writeStream 활용, 한국어 전처리 파이프라인(Kiwi + 룰베이스).

## B_project
- **설명**: 알고리즘 풀이·코딩 테스트 도구 모음과 관련 자동화 스크립트를 제공하는 프로젝트입니다.  
- **기술**: Python(라이브러리/노트북), 알고리즘 구현 모듈, FastAPI/DB 관련 운영 가이드 문서(문서화 목적).  
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT 자동화 도구 및 예제 노트북(문제 풀이·시뮬레이션), LLM 호출 유틸 변경사항(기본 모델 gpt-5→gpt-5-nano 안내).
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 987fc076ba30a27bfb802dff7977550e95b0c733 -->
