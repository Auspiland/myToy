# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 한반도(남한/북한) 좌표 또는 사각형 영역을 행정구역(시·도·시군구 등)으로 변환하고 GeoJSON으로 생성·시각화하는 도구입니다.
- **기술**: Python, shapely/STRtree 기반 공간 인덱스, GeoJSON
- **특징**: 사각형→행정구역 변환(대량 처리 최적화), 섬 지역 자동 감지 및 대표 텍스트 표기, 행정구역 경계 조회 및 GeoJSON 생성/일괄 변환

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집해 문장 전처리 후 Kafka와 OpenSearch로 업로드하는 컨테이너 기반 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리)
- **특징**: 컨테이너화된 스트리밍 아키텍처, Spark↔Kafka↔OpenSearch 연동을 통한 실시간 처리·색인화, Kiwi 기반 오탈자 수정·문장 분리 등 룰베이스 전처리

## B_project
- **설명**: 알고리즘 문제 풀이 및 코딩 테스트 자동화·보조 도구 모음 저장소입니다.
- **기술**: Python(알고리즘 라이브러리, Jupyter Notebook), FastAPI/Async 관련 가이드 및 LLM 유틸리티
- **특징**: boj_bible(자료구조·그래프·문자열·고급 알고리즘) 모듈 제공, CT 자동화·기록 도구 및 LLM 호출 유틸(기본 모델 변경 공지 포함), 예제 노트북 및 개발/배포 가이드 문서 포함
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

<!-- LAST_PROCESSED_SHA: 9500d4d4d3f62b65e1fa55669d21438fa072d6d0 -->
