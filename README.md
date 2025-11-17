# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남·북) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/GeoPandas, STRtree 공간 인덱스, GeoJSON 출력
- **특징**: 사각형→행정구역/좌표→행정구역 변환, 섬 자동 감지(비율 기반), 경계 조회 및 GeoJSON 생성/시각화

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·OpenSearch 업로드까지의 E2E 스트리밍 파이프라인입니다.
- **기술**: Docker/Docker Compose, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI, Nginx, Kiwipiepy
- **특징**: 컨테이너 기반 스트리밍 아키텍처(폴더 감시 → Spark → Kafka → OpenSearch), 대규모 전처리(오탈자 수정·문장 분리 등)와 Streaming UDF 적용, Docker 네트워크/비동기 구성

## B_project
- **설명**: 알고리즘 학습·코딩 테스트 풀이와 관련 도구들을 모아놓은 저장소입니다.
- **기술**: Python(알고리즘 라이브러리), FastAPI, 비동기 DB(PostgreSQL Async), Redis, Docker Compose, CI/CD 문서
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT(코딩 테스트) 자동화 도구 및 예제 노트북 포함, LLM 헬퍼 함수 기본 모델이 gpt-5-nano로 변경된 유틸 영향 정보
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 6e0c462da6f1fd2a23cea46cdf04b64fafb4b5b3 -->
