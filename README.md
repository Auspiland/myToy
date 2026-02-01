# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역(시/도 등)으로 빠르게 변환하고 GeoJSON으로 출력/시각화하는 도구입니다.
- **기술**: Python, Shapely/pyproj/geopandas 기반 공간처리, STRtree 공간 인덱스, GeoJSON 출력
- **특징**: 사각형→행정구역 변환(최적화된 rect2region_fast_v2), 행정경계 조회 및 GeoJSON 생성·시각화, 섬 자동 감지·대량 JSON 일괄 변환

## Mini-Pipeline
- **설명**: YouTube URL을 받아 스크립트 전처리 후 Kafka·Opensearch로 업로드하는 컨테이너화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker, Apache Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Selenium, Kiwipiepy
- **특징**: 컨테이너별 네트워크 분리·조합으로 스트리밍 처리, Spark로 파일 감시→Kafka/Opensearch 적재·전처리(문장분리·오탈자 수정), 웹 검색 UI 연동(FastAPI+Nginx)

## B_project
- **설명**: 알고리즘 문제 풀이용 라이브러리와 코딩테스트 자동화·기록 도구 모음 프로젝트입니다.
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·문자열 등), FastAPI/Async DB/Redis 기반 템플릿 문서(운영 가이드), Jupyter 노트북
- **특징**: boj_bible(알고리즘 라이브러리) 제공, CT 자동화·전처리 유틸 및 LLM 호출 유틸(기본 모델이 gpt-5-nano로 변경됨) 추가, 문제 풀이 노트북 및 운영·배포 가이드 문서 포함
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
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 7e481a3cc20d8ee15b47edd23df9da319dc4939e -->
