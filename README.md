# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, geopandas/shapely, STRtree 공간 인덱스, GeoJSON 입출력.
- **특징**: 사각형→행정구역 변환(고성능 rect2region_fast_v2), 좌표→행정구역 매핑 및 섬 자동 감지, GeoJSON 생성·일괄 변환 및 경계 조회 기능.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka 전송·Opensearch 적재까지의 컨테이너화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker(다중 컨테이너, docker-compose), Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx.
- **특징**: Streaming 기반 데이터 흐름(Kafka↔Spark↔Opensearch), Kiwipiepy+룰 기반 전처리(문장 분리·오탈자 수정), 컨테이너 네트워크 설계로 서비스 분리 및 배포 용이성.

## B_project
- **설명**: 알고리즘 문제 풀이용 라이브러리 및 코딩 테스트 자동화 도구 모음입니다.
- **기술**: Python(자료구조·그래프·트리·문자열/고급 알고리즘 모듈), 코드 자동화 스크립트, LLM 연동 유틸리티.
- **특징**: boj_bible(기본/그래프/트리/문자열/고급 알고리즘 모듈), CT 자동화 도구(문제 풀기·기록), LLM 관련 유틸 함수 기본 모델을 gpt-5에서 gpt-5-nano로 변경한 업데이트 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 2e604c43ae9f8325826274442864f7cb2d7db4bf -->
