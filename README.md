# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 입력된 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 변환해 대표 텍스트와 상세 경계 정보를 제공하는 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간색인, GeoJSON, GeoPandas(데이터 처리), GitHub 연동 스크립트.  
- **특징**: 사각형/좌표 → 시/도/시군구 변환(대량처리 지원), 섬 자동 감지·대표 표현 규칙 제공, 행정구역 경계 조회 및 GeoJSON 생성/시각화.

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트를 추출해 문장 전처리 후 Kafka와 OpenSearch로 업로드하는 Docker 기반 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker Compose, Apache Kafka(kRaft), Apache Spark Structured Streaming(PySpark), OpenSearch, FastAPI, Nginx, Selenium(스크립트 수집).  
- **특징**: 스트리밍 ingest→가공→인덱싱(재현 가능한 파이프라인), Kiwipiepy 기반 한국어 전처리(오탈자·문장 분리·불용어), 웹 검색 인터페이스 및 네트워크 분리된 컨테이너 아키텍처.

## B_project
- **설명**: 알고리즘 학습·코딩테스트용 모듈과 자동화 도구들을 모아놓은 프로젝트입니다.  
- **기술**: Python 기반 알고리즘 라이브러리 및 노트북(.ipynb), FastAPI/비동기 연동(문서화 참조), LLM 호출 유틸리티 포함.  
- **특징**: boj_bible(자료구조·그래프·트리·문자열 등) 패키지, CT 자동화·문제풀이 도구(노트북 포함), LLM 관련 유틸 및 운영·배포 가이드 문서 제공.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 1da24facae1e68af475adfc3b3487a4f8a7a0186 -->
