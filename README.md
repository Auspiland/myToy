# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->

## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 빠르게 변환하고 GeoJSON으로 출력하는 도구입니다.
- **기술**: Python, Shapely/GeoPandas 기반 공간 인덱스(STRtree), GeoJSON, LLM 보조(지명 번역), GitHub 연동 스크립트.
- **특징**: 사각형→행정구역(대표문구/상세) 변환(최적화된 rect2region_fast_v2), 섬 자동 감지 및 방향 기반 대표표현, 경계 조회·GeoJSON 생성 및 시각화.

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트를 추출해 문장 전처리 후 Kafka와 OpenSearch로 스트리밍 업로드하는 E2E 파이프라인입니다.
- **기술**: Docker-compose, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI/Nginx, KiwiPy(형태소처리), Selenium(스크립트 수집 보조).
- **특징**: 컨테이너 기반 스트리밍 파이프라인(파일→Spark→Kafka→OpenSearch), 실시간 전처리(오탈자·문장분리·불용어), 웹 검색 인터페이스 연동.

## B_project
- **설명**: 알고리즘 연습 및 코딩 테스트 자동화·기록을 위한 툴셋과 참고 자료 모음입니다.
- **기술**: Python 중심(알고리즘 라이브러리, Jupyter 노트북), FastAPI/Async 스택 문서(운영 가이드), LLM 연동 유틸.
- **특징**: boj_bible(자료구조·그래프·트리·문자열 등 모듈화된 알고리즘 모음), CT 자동화 도구(LLM 호출 유틸 포함, 기본 모델 변경 알림), 문제 풀이용 노트북/예제 코드 제공.

<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 35d3bea52714b2fb71b25f80bee8dcfea380cd5e -->
