# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## [geo_map]
- **설명**: 좌표나 사각형 영역을 대한민국(남한/북한) 행정구역으로 빠르게 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON, geopandas(데이터 처리), GitHub 연동 스크립트.
- **특징**: 사각형→행정구역(고속 버전) 변환, 행정구역 경계 조회 및 GeoJSON 생성·시각화, 섬 자동 감지 및 대량(배치) 처리 지원.

## [Mini-Pipeline]
- **설명**: YouTube 스크립트를 가져와 전처리한 뒤 Kafka·Spark·Opensearch로 업로드하는 컨테이너 기반 스트리밍 파이프라인입니다.
- **기술**: Docker(여러 compose), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI + Nginx, Kiwipiepy(한국어 전처리).
- **특징**: E2E 실시간 스트리밍 처리(Spark↔Kafka↔Opensearch), 한국어 전처리(오탈자 수정·문장 분리 등) 및 pandas_udf 적용, 웹 검색 서비스 연동(Nginx+FastAPI).

## [B_project]
- **설명**: 알고리즘 문제 풀이와 코딩 테스트 자동화 및 기록을 위한 파이썬 프로젝트 모음입니다.
- **기술**: Python 기반 라이브러리 구조(boj_bible 등), 코딩테스트 자동화 스크립트, LLM 연동 유틸리티.
- **특징**: 자료구조·그래프·문자열·고급 알고리즘 모듈(boj_bible), CT 자동화 및 기록 도구, LLM 호출 유틸(기본 모델 변경 등)
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: ce0d34526427b4ef53db2206b9626f765b3a497a -->
