# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 출력·시각화하는 도구입니다.
- **기술**: Python, shapely/STRtree, geopandas/GeoJSON, LLM(지명 번역 보조), 파일 기반 경계 데이터.
- **특징**: 사각형/좌표→행정구역 변환(빠른 v2), 섬 자동 감지 및 방향 기반 대표 표현, 경계 조회·GeoJSON 생성·일괄 변환 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집해 문장 전처리 후 Kafka와 OpenSearch로 스트리밍 업로드하는 컨테이너 기반 E2E 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy, Selenium(스크립트 수집 보조).
- **특징**: 마운트 폴더 감시→Spark로 Kafka 토픽 입력, 스트리밍 전처리(오탈자·문장분리) 및 OpenSearch 색인, 네트워크 분리된 컨테이너 구성으로 서비스 분리.

## B_project
- **설명**: 알고리즘 문제 풀이·코딩테스트 지원 라이브러리 및 자동화 도구 집합입니다.
- **기술**: Python(알고리즘 모듈, Jupyter 노트북), 코딩테스트 유틸리티, LLM 호출 유틸(응답 기본 모델 관리).
- **특징**: boj_bible(자료구조/그래프/트리/문자열 등 알고리즘 모듈), CT 자동화/기록 툴과 예제 노트북, LLM 관련 함수 기본 모델 변경 및 사용 가이드.
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

<!-- LAST_PROCESSED_SHA: 0e6f79cee4136fc2509ccbe8b6946a93fd811e8f -->
