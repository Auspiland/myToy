# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 생성·시각화하는 툴입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON 데이터, 공간 경계 데이터(행정구역).
- **특징**: 사각형→행정구역 변환(대량 처리 가능), 좌표→행정구역 변환 및 경계 조회, 섬 자동 감지·GeoJSON 생성 및 시각화

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리, Kafka·Opensearch 업로드까지의 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker/Docker Compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy(한국어 처리).
- **특징**: 컨테이너 기반 스트리밍 아키텍처, Spark로 Kafka↔Opensearch 파이프라인 처리, Kiwi 기반 오탈자 수정·문장 분리·불용어 처리

## B_project
- **설명**: 알고리즘 학습·코딩테스트 지원용 모음(라이브러리 및 자동화 도구)입니다.
- **기술**: Python 기반 알고리즘 구현 모듈, 유틸 스크립트, LLM 연동 유틸(CT 자동화).
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT 자동화 및 기록 도구, LLM 호출유틸의 기본 모델 설정 변경 안내 (gpt-5 → gpt-5-nano)
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: b1c81464869b839e392e0a2cf5da5c8a54a04d57 -->
