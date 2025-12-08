# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 한반도(남/북한) 행정구역(시/도/시군구 등)으로 변환합니다.
- **기술**: Python, Shapely(STRtree) 기반 공간 인덱싱, GeoJSON 입출력.
- **특징**: 사각형→행정구역 변환(대표 표현 포함), 대량 처리용 convert_many(고성능), 경계 조회·GeoJSON 생성 및 섬 자동 감지.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집·전처리하여 Kafka와 OpenSearch로 스트리밍 저장하는 E2E 파이프라인입니다.
- **기술**: Docker(Compose), Apache Spark(streaming), Kafka(kRaft), OpenSearch, FastAPI/Nginx.
- **특징**: 컨테이너화된 스트리밍 처리, Kiwipiepy 기반 문장 전처리(pandas_udf 사용), Kafka↔OpenSearch 연동 및 웹 검색 인터페이스.

## B_project
- **설명**: 알고리즘 문제 풀이와 코딩 테스트 자동화 도구들을 모아둔 프로젝트입니다.
- **기술**: Python 기반 알고리즘 라이브러리, Jupyter 노트북, FastAPI/비동기 유틸(문서 참조).
- **특징**: boj_bible 알고리즘 모듈(자료구조/그래프/트리/문자열 등), CT 자동화·기록 툴(LLM 호출 유틸 포함), 예제 노트북 및 배포 가이드 문서.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 2574b4620e5d5f07f8dcd9299dee39708dee1c88 -->
