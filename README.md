# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표나 사각형 영역을 대한민국(남한/북한) 행정구역으로 빠르게 매핑하고 GeoJSON으로 출력하는 도구입니다.
- **기술**: Python, Shapely/GeoPandas, STRtree 공간 인덱스, GeoJSON 파일 및 GitHub 연동.
- **특징**: 사각형·포인트→행정구역 변환(고성능 rect2region_fast_v2), 섬 자동 감지·방향 기반 대표표현 생성, 행정구역 경계 조회 및 GeoJSON 생성/일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·Kafka·OpenSearch 업로드까지의 컨테이너화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI + Nginx, Kiwipiepy(한국어 전처리).
- **특징**: 마운트 폴더→Spark readStream으로 ingest→Kafka 토픽/Opensearch 인덱싱, Kiwipiepy 기반 오탈자·문장 분리 전처리, 웹 검색용 FastAPI 연동.

## B_project
- **설명**: 알고리즘 학습·코딩 테스트용 라이브러리와 자동화 도구 모음입니다.
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열 등), Jupyter 노트북, LLM 유틸리티(응답 함수).
- **특징**: boj_bible(기초·그래프·트리·문자열·고급 알고리즘) 구성, CT 자동화 및 LLM 연동 유틸(기본 모델 변경 안내 포함), 문제 풀이용 예제 노트북 제공.
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

<!-- LAST_PROCESSED_SHA: 43889c0474f338a95b6ef14f55173dfd0ba2cc22 -->
