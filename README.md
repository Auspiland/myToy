# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 한반도(남·북)에서 주어진 좌표 또는 사각형 영역을 행정구역(시/도/군 등)으로 판정하고 GeoJSON으로 시각화/내보내는 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 인덱스, GeoJSON 처리(파일 생성/조회), 표준 공간 데이터(행정구역 GeoJSON).
- **특징**: 사각형·단일 좌표→행정구역 변환(대표문구 생성 포함), 섬 자동 감지 및 방향 기반 표현, 경계 조회 및 GeoJSON 일괄 변환/시각화.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집·전처리해 Kafka·Spark·Opensearch로 스트리밍 처리하고 웹에서 검색/조회 가능한 E2E 파이프라인입니다.
- **기술**: Docker(멀티 컨테이너), Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Selenium, Kiwipiepy.
- **특징**: Streaming 기반 데이터 수집·전처리(오탈자 수정·문장 분리·불용어 처리), Spark↔Kafka↔Opensearch 연동, 도커 컴포즈로 네트워크 분리된 서비스 구성.

## B_project
- **설명**: 알고리즘 연습과 코딩 테스트 자동화·기록을 위한 코드 모음 및 유틸리티 모듈입니다.
- **기술**: Python 기반 알고리즘/자료구조 라이브러리(스택/큐/그래프/트리/문자열/네트워크플로우 등).
- **특징**: boj_bible(백준 풀이용 모듈) 제공, CT(코딩 테스트 자동화·기록) 도구 포함, LLM 관련 유틸의 기본 모델 변경 안내(문서화).
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: c6f501ee030dcf8881d15b737fbcd83eabaa7522 -->
