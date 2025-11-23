# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국·북한 행정구역으로 변환하고 GeoJSON으로 생성·시각화하는 도구입니다.
- **기술**: Python, Shapely(STRtree) 기반 공간 인덱스, GeoJSON, 행정구역 데이터셋, 일부 LLM(지명 번역).
- **특징**: 빠른 Rect→Region 변환(rect2region_fast_v2), 섬 자동 감지 및 방향 기반 대표문구 생성, 행정구역 경계 조회·GeoJSON/배치 변환 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 → 문장 전처리 → Kafka/Opensearch 업로드까지의 컨테이너화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker(Compose), Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Selenium, Kiwipiepy.
- **특징**: 각 서비스별 컨테이너 분리된 스트리밍 구성, Spark↔Kafka↔Opensearch 데이터 흐름 및 마운트 기반 입력 처리, 한국어 전처리(Kiwipiepy) 유틸 및 Pandas UDF 적용.

## B_project
- **설명**: 알고리즘 문제 풀이와 코딩 테스트 자동화·기록을 위한 도구 모음 프로젝트입니다.
- **기술**: Python 중심(라이브러리·Jupyter), 알고리즘/자료구조 모듈, CT 자동화 유틸(LLM 연동), Docker/웹 운영 관련 문서화.
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT 자동화 및 LLM 호출 유틸(기본 모델 변경 알림 포함), kakao_history 노트북·운영·배포 가이드 문서 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: dd45455a19a794c144adbbf521b896d9af8ceb07 -->
