# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역(시/도 등)으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간인덱스, GeoJSON, GitHub 연동 스크립트.  
- **특징**: 사각형→행정구역 변환(대표문구/상세), 좌표→지역 변환 및 섬 자동 감지, GeoJSON 생성·일괄 JSON 변환 및 경계 조회.

## Mini-Pipeline
- **설명**: Youtube 스크립트 추출 → 문장 전처리 → Kafka/Opensearch 업로드까지의 E2E 스트리밍 파이프라인(도커 기반)입니다.  
- **기술**: Docker Compose(멀티 컨테이너), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리).  
- **특징**: 마운트 폴더 기반 파일 감시→Spark→Kafka 토픽 파이프라인, Kiwipiepy 기반 오탈자·문장분리 처리(udf 적용), 컨테이너 네트워크·배포 구성 예제 포함.

## B_project
- **설명**: 알고리즘 문제 풀이·코딩 테스트 연습용 모음(라이브러리·노트북·유틸).  
- **기술**: Python, Jupyter 노트북, 알고리즘 모듈(자료구조·그래프·문자열·고급 알고리즘), LLM 유틸 통합.  
- **특징**: boj_bible(기본/그래프/트리/문자열/고급 모듈), CT 자동화 도구 및 예제 노트북(문제 풀이 함수), LLM 헬퍼 기본 모델 변경 등 운영·개발 유틸 자료 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 69da4657f7a3b0a2c09662a463f639385e2747d6 -->
