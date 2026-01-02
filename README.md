# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 한반도(남·북) 행정구역으로 변환하고 GeoJSON으로 생성/시각화하는 도구  
- **기술**: Python, Shapely/GEOS, STRtree 공간 인덱스, GeoJSON 데이터(대한민국/북한), pip 패키지 기반  
- **특징**: 사각형·좌표→행정구역 변환(대표문구/상세); 섬 자동 감지 및 방향 기반 대표표현 규칙; GeoJSON 생성·대량 JSON 일괄 변환

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 후 전처리하여 Kafka→Spark→Opensearch로 스트리밍 적재하는 컨테이너화된 E2E 파이프라인  
- **기술**: Docker Compose, Kafka(kRaft), Apache Spark Structured Streaming, OpenSearch, FastAPI, Nginx, Kiwipiepy, Selenium(수집 보조)  
- **특징**: 컨테이너 기반의 네트워크 분리된 스트리밍 아키텍처; Spark로 실시간 전처리(Kiwi + 룰베이스) 및 토픽/인덱스 적재; Nginx+FastAPI로 검색 UI 제공

## B_project
- **설명**: 알고리즘 문제 풀이·코딩 테스트 연습용 라이브러리와 자동화 도구 모음(백준 지원 포함)  
- **기술**: Python(자료구조·그래프·트리·문자열·고급 알고리즘), Jupyter 노트북, FastAPI/비동기 운영 가이드 문서화  
- **특징**: boj_bible(기초·그래프·트리·문자열·고급 알고리즘) 모듈; CT 자동화 도구 및 kakao_history.ipynb 예제; LLM 관련 기본 모델 변경 안내(gpt-5 → gpt-5-nano)
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

<!-- LAST_PROCESSED_SHA: f4333a1b1d8685d671995feca0c45fd548d455cf -->
