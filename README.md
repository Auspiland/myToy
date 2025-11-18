# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 단일 좌표를 대한민국(남·북 포함) 행정구역으로 매핑하고 GeoJSON으로 출력·시각화하는 도구.
- **기술**: Python, geopandas/shapely, STRtree 공간 인덱스, GeoJSON, Fiona 등 GIS 라이브러리.
- **특징**: 사각형→행정구역(대표 텍스트/상세) 변환(최적화된 rect2region_fast_v2), 섬 지역 자동 감지 및 방향 기반 대표 표현, 행정구역 경계 조회·GeoJSON 생성·일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출을 시작으로 문장 전처리 후 Kafka/Opensearch로 적재하는 Docker 기반 E2E 스트리밍 파이프라인.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Kiwipiepy(한국어 전처리), Selenium(데이터 수집 보조).
- **특징**: 컨테이너화된 스트리밍 파이프라인(파일 감시 → Spark → Kafka → Opensearch), 한국어 전처리(UDF 형태의 Kiwi 적용) 및 실시간 색인/검색, 멀티네트워크 구성으로 서비스 분리.

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트 자동화용 유틸리티와 풀이 모음 프로젝트.
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열·고급 알고리즘), Jupyter 노트북, FastAPI/LLM 유틸(프로젝트 내 도구).
- **특징**: boj_bible로 정리된 알고리즘 라이브러리(기본/그래프/트리/문자열/고급), CT 자동화·기록 도구 및 예제 노트북(kakao_history) 제공, LLM 호출 유틸의 기본 모델 변경 등 운영·개발 보조 기능.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: a0221308e27055de73d0e3811093e8209b516c24 -->
