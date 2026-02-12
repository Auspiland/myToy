# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역(시·도 등)으로 빠르게 변환하고 GeoJSON으로 출력/시각화하는 툴입니다.  
- **기술**: Python, Shapely/GeoPandas 기반 공간 인덱스(STRtree), GeoJSON, 공간 경계 데이터(행정구역 shapefile/geojson).  
- **특징**: 고성능 rect→region 변환(최적화된 rect2region_fast_v2), 섬 지역 자동 감지 및 대표 텍스트 규칙 적용, GeoJSON 생성·일괄 변환 및 경계 조회 기능.

## Mini-Pipeline
- **설명**: YouTube 스크립트 수집부터 문장 전처리·Kafka 전송·Opensearch 업로드까지 Docker 기반 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker / docker-compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Selenium, Kiwipiepy(한국어 전처리).  
- **특징**: 컨테이너화된 스트리밍 파이프라인(파일 감시 → Kafka 토픽 → Spark 처리 → Opensearch 저장), Kiwipiepy 기반 텍스트 정제(pandas_udf 활용), 네트워크 분리로 구성된 서비스 연동 및 모니터링·디버깅 지원.

## B_project
- **설명**: 알고리즘 연습과 코딩 테스트 자동화·도구 모음(백준 풀이 라이브러리 및 CT 도구).  
- **기술**: Python 중심(알고리즘 모듈, Jupyter 노트북), FastAPI/Async 구성 문서(운영 가이드 참조).  
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈화, CT 자동화용 유틸과 LLM 연동 함수(기본 모델 변경 안내 포함), kakao_history 등 실전 예제 노트북 포함.
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

<!-- LAST_PROCESSED_SHA: 413934450d1ce19b0c30880de105bea85f0ed330 -->
