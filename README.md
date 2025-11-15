# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 한반도 행정구역(시/도/시군구 등)으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely/GeoPandas, STRtree 공간 인덱싱, GeoJSON.  
- **특징**: 사각형→행정구역·좌표 변환(대표 문구 지원), 섬 자동 감지 및 대표표현 규칙, 행정경계 조회·GeoJSON 생성·일괄 변환 지원.

## Mini-Pipeline
- **설명**: YouTube URL에서 스크립트를 추출해 문장 전처리 후 Kafka와 OpenSearch로 업로드하는 스트리밍 기반 E2E 파이프라인입니다.  
- **기술**: Docker Compose, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI/Nginx, Selenium, Kiwipiepy.  
- **특징**: Streaming 기반 Spark→Kafka→OpenSearch 파이프라인 구현, Kiwipiepy+pandas_udf를 이용한 한글 전처리(오탈자·문장분리 등), Docker 네트워크와 Nginx/FastAPI를 통한 검색 UI 연동.

## B_project
- **설명**: 알고리즘 문제 풀이 및 코딩 테스트 자동화·도구를 모아놓은 프로젝트입니다.  
- **기술**: Python(알고리즘 라이브러리·노트북), Jupyter, FastAPI/DB 관련 운영 문서.  
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈 제공, CT 자동화 도구 및 LLM 래퍼(기본 모델이 gpt-5-nano로 변경), 문제 풀이 노트북(예: kakao_history) 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 0139fbedb3d90e60ee136326f5740f85cd6d49a9 -->
