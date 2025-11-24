# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 한반도(남·북) 행정구역으로 빠르게 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely/GeoPandas, STRtree 공간인덱스, GeoJSON  
- **특징**: 사각형→행정구역(광역/시군구) 변환(고성능 v2), 섬 자동 감지 및 방향 기반 대표 표현, 경계 조회·GeoJSON 생성·일괄 변환 지원

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 → 문장 전처리 → Kafka/Opensearch 업로드까지의 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker Compose, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy  
- **특징**: Spark 기반 스트리밍 ETL(폴더 감시→Kafka 토픽), 한국어 전처리(Kiwipiepy + 규칙) 및 페이로드 변환, OpenSearch 연동으로 검색/웹 노출 지원

## B_project
- **설명**: 알고리즘 학습·코딩테스트 풀이와 관련 도구(라이브러리·노트북·자동화)를 모아둔 프로젝트입니다.  
- **기술**: Python, Jupyter Notebook, 알고리즘/자료구조 구현, LLM 호출 유틸리티  
- **특징**: boj_bible(기초·그래프·트리·문자열·고급 알고리즘) 모듈화, CT 자동화·기록 도구 및 LLM 응답 유틸 제공, 문제 풀이 예제 노트북(.ipynb) 및 운영·개발 가이드 문서 포함
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 4cb4a074fa63d0f7ad205947c6cb9030d92e7ac5 -->
