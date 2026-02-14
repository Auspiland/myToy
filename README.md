# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국/북한 행정구역(시/도 등)으로 변환하고 GeoJSON으로 출력·시각화하는 도구입니다.  
- **기술**: Python (shapely/STRtree 기반 공간 인덱스), GeoJSON, geopandas 관련 도구.  
- **특징**: 사각형→행정구역 변환(고성능 rect2region_fast_v2), 섬 자동 감지 및 방향 기반 대표 표현, 행정구역 경계 조회·GeoJSON 생성 및 일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 후 문장 전처리하여 Kafka와 OpenSearch로 업로드하는 Docker 기반 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker Compose, Spark Structured Streaming, Kafka (kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리).  
- **특징**: 마운트 폴더 감시→Spark로 Kafka 토픽 생성·가공·인덱싱, Kiwipiepy 기반 오탈자 수정·문장 분리(udf/pandas_udf 사용), 컨테이너화된 서비스 간 내부 네트워크 구성 및 웹 검색 인터페이스 연동.

## B_project
- **설명**: 알고리즘 학습·코딩테스트 풀이용 라이브러리 및 자동화 도구 모음입니다.  
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열·고급 알고리즘), FastAPI/Async 관련 가이드 문서 및 노트북(.ipynb).  
- **특징**: boj_bible(기본·그래프·트리 등 알고리즘 모듈), CT(코딩테스트 자동화) 및 LLM 헬퍼 변경사항(gpt-5 → 기본 gpt-5-nano), kakao_history 등 문제 풀이 노트북 포함.
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
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: bbffb660f75b6fc87301b391cfbd9f8bda939edf -->
