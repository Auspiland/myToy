# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남/북 포함)의 행정구역으로 빠르게 변환하고 GeoJSON으로 출력하는 도구입니다.
- **기술**: Python, Shapely/GeoPandas, STRtree 공간인덱스, GeoJSON
- **특징**: 사각형→행정구역 변환(최적화된 rect2region_fast_v2), GeoJSON 생성 및 시각화(결과 파일 GitHub 푸시 포함), 행정구역 경계 조회 및 섬 자동 감지

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트 수집 후 문장 전처리하여 Kafka·OpenSearch로 스트리밍 적재하는 E2E 파이프라인입니다.
- **기술**: Docker(컨테이너화), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Kiwipiepy
- **특징**: 컨테이너 기반의 스트리밍 파이프라인(파일 감시→Kafka 토픽→가공→OpenSearch), 한국어 전처리(Kiwi + pandas_udf) 및 검색 서비스 연동, 운영용 Docker Compose 네트워킹 구성

## B_project
- **설명**: 알고리즘 문제 풀이 및 코딩 테스트 자동화·도구 모음 저장소입니다.
- **기술**: Python, 알고리즘 라이브러리 모듈화, Jupyter 노트북, FastAPI/Async 관련 유틸(문서 참고)
- **특징**: boj_bible(자료구조·그래프·트리·문자열 등 알고리즘 모듈), CT 자동화 도구(LLM 연동 유틸 포함, 기본 모델 gpt-5-nano로 변경 안내), 예제 노트북(kakao_history) 및 개발/배포 가이드 문서 포함
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 6caaa787ea1b65e6c3411fc638a79002512826aa -->
