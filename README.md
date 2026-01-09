# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국 행정구역(시/도/시군구 등)으로 변환하고 GeoJSON으로 시각화하는 도구  
- **기술**: Python, geopandas/shapely, STRtree(공간 인덱스), GeoJSON  
- **특징**: 사각형→행정구역 변환(대량 처리 최적화), 좌표→행정구역/경계 조회 및 GeoJSON 생성, 섬 자동 감지 및 방향 기반 대표 표현

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·Spark·OpenSearch 업로드까지의 컨테이너화된 스트리밍 E2E 파이프라인  
- **기술**: Docker Compose, Apache Kafka, Apache Spark(Structured Streaming), OpenSearch, FastAPI, Nginx, Kiwipiepy, Selenium  
- **특징**: 컨테이너별 분산 아키텍처(웹→Nginx→FastAPI→Spark→Kafka→OpenSearch), 한국어 전처리(Kiwipiepy + 룰베이스)와 파일 감시 기반 파이프라인 처리, Docker 환경에서의 스트리밍 운영·디버깅 구성

## B_project
- **설명**: 알고리즘 문제 풀이(BOJ)용 라이브러리와 코딩 테스트 자동화·기록 도구 모음  
- **기술**: Python, Jupyter Notebook, (프로젝트 문서화에 FastAPI/Async·Postgres/Redis 등 언급)  
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT 자동화 도구 및 LLM 헬퍼 함수(기본 모델 변경 안내 포함), 문제 풀이 노트북 및 운영·배포 가이드 문서
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

<!-- LAST_PROCESSED_SHA: ef93ad72ccc2ac55b5734a346960f9909328f328 -->
