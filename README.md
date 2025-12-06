# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역 단위로 변환·분석하여 결과를 반환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely/GeoPandas 기반 공간 인덱스(STRtree), GeoJSON 입출력.  
- **특징**: 사각형→행정구역 변환(대표문구/상세), 좌표→행정구역 변환 및 경계 조회, 섬 자동 감지 및 GeoJSON 생성/일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집해 문장 전처리 후 Kafka와 OpenSearch에 적재하는 E2E 스트리밍 파이프라인입니다.  
- **기술**: Docker(컨테이너화), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리).  
- **특징**: Spark readStream/writeStream 기반 실시간 파이프라인, Kafka 토픽을 통한 메시지 흐름 및 Opensearch 색인, Kiwipiepy+룰 기반 처리(오탈자/문장분리/불용어).

## B_project
- **설명**: 알고리즘 연습·코딩테스트 풀이를 위한 라이브러리와 자동화 도구 모음입니다.  
- **기술**: Python(모듈/노트북), 코딩 테스트 알고리즘 구현, LLM 유틸(common_utils) 통합.  
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT 자동화 도구 및 노트북(kakao_history) 포함, LLM 관련 함수 기본 모델 변경 등 운영·개발 가이드 문서 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 0fed109f4a78b5402104a14b25579434fc086e43 -->
