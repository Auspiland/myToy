# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 매핑하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, GeoPandas/Shapely, STRtree 공간색인, GeoJSON 처리
- **특징**: 사각형↔행정구역 변환(대량 처리 최적화), 섬 지역 자동 감지 및 방향 기반 대표 표현, 행정구역 경계 조회·GeoJSON 생성

## Mini-Pipeline
- **설명**: Youtube 스크립트 추출부터 전처리→Kafka→Spark→Opensearch까지 이어지는 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker/compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Kiwipiepy
- **특징**: 컨테이너화된 스트리밍 아키텍처(마운트 폴더 감시→Kafka 토픽), 텍스트 전처리(오탈자·문장분리·불용어) 파이프라인, 웹 검색 인터페이스와 연동

## B_project
- **설명**: 알고리즘 연습(백준) 및 코딩 테스트 자동화·도구 모음 프로젝트입니다.
- **기술**: Python 기반 알고리즘 라이브러리·노트북, FastAPI/Async 문서(운영 가이드), LLM 연동 유틸리티
- **특징**: boj_bible(자료구조·그래프·문자열 등) 모듈, CT 자동화·문제 풀이 유틸 및 예제 노트북(kakao_history), LLM 호출 유틸의 기본 모델 변경 안내 (gpt-5 → gpt-5-nano)
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 72c9dd737e9c06c922a4acc27ebfb226762cd549 -->
