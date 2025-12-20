# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역(시/도 등)으로 빠르게 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, shapely/STRtree 기반 공간 인덱스, GeoJSON, geopandas/파이썬 패키지 생태계.  
- **특징**: 사각형→행정구역 변환 및 대량 처리(convert_many), 좌표→행정구역 변환과 경계 조회(get_region_boundary), 섬 자동 감지·GeoJSON 생성 및 시각화.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리, Kafka 및 OpenSearch로의 업로드까지 Docker화된 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker/Docker Compose, Apache Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI + Nginx, Kiwipiepy(한국어 전처리).  
- **특징**: 마운트 폴더 감시(readStream)→Kafka 토픽 처리→OpenSearch 색인, Kiwipiepy 기반 오탈자 수정·문장분리( pandas_udf 활용 ), 컨테이너별 네트워크 구성으로 서비스 분리.

## B_project
- **설명**: 알고리즘 문제 풀이용 라이브러리와 코딩 테스트 자동화/기록 도구를 모아둔 프로젝트입니다.  
- **기술**: Python(알고리즘 모듈), Jupyter 노트북 예제, FastAPI/문서화(운영 가이드 문서 포함).  
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT 자동화 도구 및 예제 노트북(B_project/CT/kakao_history.ipynb), LLM 연동 유틸(common_utils) 기본 모델 변경 안내(기본 gpt-5-nano).
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

<!-- LAST_PROCESSED_SHA: 52bf18edb8fbef66ad8ab70f7d681541e7b403dd -->
