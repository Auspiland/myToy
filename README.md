# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## [geo_map]
- **설명**: 사각형 영역이나 단일 좌표를 한반도(남/북) 행정구역으로 매핑하고 GeoJSON으로 생성·시각화하는 파이썬 기반 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON, 공간 경계 데이터, LLM(지명 번역) 및 GitHub 자동화.
- **특징**: 고성능 rect→region 변환(rect2region_fast_v2) 및 배치 처리, 섬 자동 감지·대표 표현 규칙(면적/방향 기반), 행정구역 경계 조회 및 GeoJSON 생성/시각화.

## [Mini-Pipeline]
- **설명**: Youtube 스크립트 추출부터 문장 전처리·Kafka 전송·Spark 처리·Opensearch 업로드까지의 Docker 기반 E2E 스트리밍 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Kiwipiepy(한국어 전처리), Selenium(스크래핑 보조).
- **특징**: 컨테이너화된 멀티서비스 네트워크 구성(서비스별 compose), Kafka 토픽 기반 스트리밍 파이프라인 및 Spark 처리(udf/pandas_udf 활용), Opensearch 연동과 웹 검색 인터페이스 연동.

## [B_project]
- **설명**: 알고리즘·코딩테스트 연습 및 자동화 도구 모음(문제 풀이 라이브러리·CT 자동화·유틸).
- **기술**: Python 기반 알고리즘 라이브러리(자료구조, 그래프, 트리, 문자열, 고급 알고리즘), Jupyter 노트북, (문서 기준) FastAPI·비동기 DB/Redis 연동 관련 스택.
- **특징**: boj_bible(자료구조·알고리즘 카테고리) 제공, CT 자동화 및 LLM 유틸(기본 모델이 gpt-5→gpt-5-nano로 변경된 알림 포함), 재사용 가능한 노트북 예제 및 운영·배포 가이드 문서.
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
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: e0b63a63090bc7228394407d49cf7f9760e7bf0c -->
