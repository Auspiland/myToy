# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## [geo_map]
- **설명**: 사각형 영역 또는 좌표를 대한민국(남·북 포함) 행정구역으로 변환하고 GeoJSON으로 생성·시각화하는 파이썬 지리공간 도구.  
- **기술**: Python, Shapely/GeoPandas(STRtree 기반 공간색인), GeoJSON, LLM(지명 번역 보조).  
- **특징**: 사각형→행정구역 변환(대표 표현·면적 기준), 섬 자동 감지 및 방향 기반 대표문구 생성, 행정구역 경계 조회·GeoJSON 일괄 변환·시각화.

## [Mini-Pipeline]
- **설명**: YouTube 스크립트 수집 → 전처리 → Kafka/Spark 스트리밍 → OpenSearch 인덱싱으로 이어지는 컨테이너화된 E2E 파이프라인.  
- **기술**: Docker/docker-compose, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy, Selenium(수집 보조).  
- **특징**: 마운트된 폴더/JSON 기반 스트리밍 입력 감시 및 Kafka 토픽 연동, 한국어 전처리(오탈자 수정·문장분리 등) 병렬 처리, OpenSearch 연동 및 웹 검색 인터페이스 제공.

## [B_project]
- **설명**: 알고리즘 문제 풀이·코딩 테스트 지원용 라이브러리와 도구(예제 노트북 및 운영 가이드 포함).  
- **기술**: Python, Jupyter Notebook, 알고리즘/자료구조 모듈, (서비스 가이드를 위한) FastAPI/비동기 스택 문서화.  
- **특징**: boj_bible(기초·그래프·트리·문자열·고급) 모듈 집합, CT 자동화 도구 및 LLM 연동 유틸(기본 모델 gpt-5-nano로 변경 안내 포함), kakao_history 등 실전 풀이 노트북 및 운영·배포 가이드 제공.
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

<!-- LAST_PROCESSED_SHA: e310a96aca68b203aa2ff45cee339d00f7cfc659 -->
