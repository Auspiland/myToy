# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국/북한의 행정구역(시·도 등)으로 변환하는 GIS 도구입니다.
- **기술**: Python, GeoJSON, Shapely/STRtree(Spatial Index), 공간 데이터(GeoJSON) 처리 도구.
- **특징**: 사각형·좌표→행정구역 변환, 섬 지역 자동 감지 및 대표 문구 생성, GeoJSON 생성·대량(파일) 변환 및 경계 조회.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·Kafka 송신·Opensearch 적재까지의 컨테이너화된 스트리밍 파이프라인입니다.
- **기술**: Docker Compose(멀티컨테이너), Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Selenium, Kiwipiepy.
- **특징**: Streaming 기반 E2E 파이프라인(Kafka↔Spark↔Opensearch), 한국어 전처리(키위·룰베이스) 및 pandas_udf 병렬 처리, 컨테이너 네트워크·서비스 라우팅 구성.

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트 자동화·도움 도구 모음입니다.
- **기술**: Python 기반 알고리즘 라이브러리 및 유틸 모듈(자료구조·그래프·트리·문자열·고급 알고리즘).
- **특징**: boj_bible(기초/그래프/트리/문자열/고급) 모듈 집합, CT(코딩 테스트) 자동화·기록 도구, LLM 호출 유틸(기본 모델 변경 및 스트리밍 헬퍼) 관련 설정 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 28251b78e64cb82ffdbdba39a91b0c7915f92ce6 -->
