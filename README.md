# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 관련 GeoJSON을 생성·시각화하는 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON, GitHub 연동 (pip로 설치 가능한 의존성).
- **특징**: 사각형/좌표→행정구역 변환(대량 처리 지원), 행정구역 경계 조회·GeoJSON 생성 및 시각화, 섬 자동 감지 및 대표 텍스트 생성.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집해 문장 전처리 후 Kafka·Opensearch에 업로드하는 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker(Compose) 기반 컨테이너 아키텍처, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy.
- **특징**: Spark+Kafka를 이용한 실시간 ETL 파이프라인, Kiwipiepy·룰베이스 기반 텍스트 전처리(오탈자 수정·문장 분리), Opensearch 인덱싱 및 웹 검색 연동.

## B_project
- **설명**: 알고리즘 연습·코딩 테스트 지원을 위한 코드베이스 및 도구 모음입니다.
- **기술**: Python 기반 알고리즘 라이브러리 및 유틸(노트북 포함), FastAPI/Async 도구 문서(참고용).
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT 자동화·LLM 연동 유틸(기본 모델 변경 안내 포함), 예제 문제 풀이 노트북(.ipynb) 제공.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 4f6bb4b464760a5f5cfe0f870ca038d90898ffcd -->
