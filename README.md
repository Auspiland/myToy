# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python 기반(Shapely/STRtree 기반 공간 인덱스), GeoJSON, 공간 데이터 처리 라이브러리 및 일부 LLM 활용(지명 번역).  
- **특징**: 사각형→행정구역/좌표→행정구역 변환, 섬 자동 감지 및 방향 기반 대표 표현 생성, 변환 결과를 GeoJSON으로 생성·시각화·일괄처리.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 후 전처리하여 Kafka → Spark 스트리밍 → Opensearch로 업로드하는 E2E 파이프라인(도커 컨테이너화).  
- **기술**: Docker / docker-compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리).  
- **특징**: 컨테이너 기반 스트리밍 파이프라인(파일 감시 → Kafka 토픽 → Spark 처리 → Opensearch 색인), 실시간 텍스트 전처리(오탈자 보정·문장 분리) 및 웹 검색 인터페이스 연동.

## B_project
- **설명**: 알고리즘 학습·코딩테스트용 레퍼지토리 및 자동화 도구 모음입니다.  
- **기술**: Python 중심(라이브러리/노트북 형태), Jupyter 노트북, CT 자동화 유틸(LLM 호출 유틸 포함).  
- **특징**: boj_bible(자료구조·알고리즘 모듈) 및 CT 자동화 도구, 알고리즘 풀이 예제‧노트북(변환하여 모듈화 가능)과 LLM 연동 유틸 문서 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 45975da193e5759cf584b756291e0f742dbb68b7 -->
