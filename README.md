# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 생성·시각화하는 도구입니다.  
- **기술**: Python, shapely/GeoPandas, STRtree 공간 인덱스, GeoJSON 파일 입출력.  
- **특징**: 사각형→행정구역(대표문구/상세) 변환, 섬 지역 자동 감지 및 행정구역 경계 조회, GeoJSON 생성·대량 JSON 일괄 변환.

## Mini-Pipeline
- **설명**: YouTube URL을 받아 문장 전처리 후 Kafka와 OpenSearch로 업로드하는 Docker 기반 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker 컨테이너화, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI 및 Nginx.  
- **특징**: 컨테이너 간 네트워크 기반 모듈형 아키텍처, Spark로 파일 감시→Kafka 토픽 파이프라인→OpenSearch 색인, Kiwipiepy·룰베이스 기반 한국어 전처리(문장 분리·오탈자 수정 등).

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트 해결을 위한 코드 집합과 자동화 도구입니다.  
- **기술**: Python 기반 모듈형 라이브러리(문제 풀이·자료구조·알고리즘 구현).  
- **특징**: boj_bible(스택/큐/그래프/트리/문자열/고급 알고리즘 구현), CT 모듈(코딩 테스트 자동화 및 기록 도구).
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: aefb826a2abdd5b7bc651c66a777f6a58b8fb1c6 -->
