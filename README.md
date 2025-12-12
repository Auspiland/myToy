# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국/북한 행정구역(시/도/시군구 등)으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely(STRtree) 기반 공간 색인, GeoJSON 처리, GitHub 연동 스크립트.
- **특징**: 사각형→행정구역 변환 및 다건 일괄처리, 섬 자동 감지 및 방향 기반 대표표현, 경계 조회·GeoJSON 생성 및 시각화.

## Mini-Pipeline
- **설명**: YouTube URL에서 스크립트를 추출해 문장 전처리 후 Kafka와 OpenSearch로 스트리밍 업로드하는 E2E 파이프라인입니다.
- **기술**: Docker/compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI + Nginx, Kiwipiepy(한국어 전처리).
- **특징**: 컨테이너 기반의 스트리밍 아키텍처, Kiwi 기반 오탈자 수정·문장 분리·불용어 처리(pandas_udf), Kafka 토픽과 OpenSearch 연동으로 실시간 검색 가능.

## B_project
- **설명**: 알고리즘 문제 풀이용 라이브러리 및 코딩 테스트 자동화·기록 도구 모음입니다.
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열 등), 노트북/스크립트 예제, LLM 연동 유틸리티.
- **특징**: boj_bible(기초·그래프·트리·문자열·고급 알고리즘) 모듈, CT 자동화와 LLM 헬퍼(기본 모델이 gpt-5-nano로 변경됨) 및 문제별 예제 노트북/운영 가이드.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: e20a4665098ef172752c7b635d947bd92f413f10 -->
