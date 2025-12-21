# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 매핑하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python (shapely/GeoPandas 기반), STRtree 공간 인덱스, GeoJSON 출력
- **특징**: 사각형→행정구역 변환(대표문구/상세), 섬 자동 감지(지역 방향 기반 표현), 행정구역 경계 조회 및 GeoJSON 생성/일괄 변환

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·Kafka 전송·Opensearch 색인까지의 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Apache Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy
- **특징**: Spark readStream 기반의 스트리밍 처리·Kafka 토픽 연동, Kiwipiepy/pandas_udf를 이용한 텍스트 전처리(오탈자/문장분리), Opensearch 색인 및 웹 검색 연동

## B_project
- **설명**: 알고리즘 연습 및 코딩 테스트 지원을 위한 파이썬 라이브러리·도구 모음입니다.
- **기술**: Python 기반 알고리즘 구현(자료구조·그래프·트리·문자열 등), Jupyter 노트북 및 FastAPI 관련 문서
- **특징**: boj_bible(기본·그래프·트리·문자열·고급 알고리즘 모듈), CT 자동화·LLM 헬퍼(기본 모델 변경 알림 포함), 예제 노트북(kakao_history) 및 운영 가이드 문서 제공
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 2539fca9776729e92ad7e6596e3154696a90e002 -->
