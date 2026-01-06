# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남/북한 포함) 행정구역으로 변환하고 결과를 GeoJSON으로 생성·시각화하는 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON, geopandas 스타일 데이터 처리.  
- **특징**: 사각형/단일 좌표 → 행정구역 변환(최적화된 rect2region_fast_v2), 섬 자동 감지 및 방향 기반 대표 표현, GeoJSON 생성·대량 JSON 변환 및 경계 조회 기능.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 입력으로 받아 문장 전처리 후 Kafka → Spark → Opensearch로 업로드하는 도커화된 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker / docker-compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Selenium, Kiwipiepy.  
- **특징**: 컨테이너 기반 멀티 네트워크 아키텍처로 스트리밍 파이프라인 구성, Kiwipiepy+pandas_udf로 한국어 전처리(오탈자·문장분리·불용어), Kafka/Opensearch 연동 및 실시간 인덱싱/검색 제공.

## B_project
- **설명**: 알고리즘 문제 풀이 및 코딩 테스트 자동화·기록을 위한 도구 모음입니다.  
- **기술**: Python 기반 알고리즘 라이브러리·유틸, Jupyter 노트북 예제, LLM 호출 유틸(응답 헬퍼).  
- **특징**: 백준용 모듈(자료구조·그래프·트리·문자열·고급 알고리즘) 모음, CT 자동화용 유틸과 예제 노트북(kakao_history.ipynb), LLM 호출 helper의 기본 모델 변경 등 운영·재사용성 문서 포함.
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

<!-- LAST_PROCESSED_SHA: 34d71c556e63a214c65589d4b3b75334f5ff6296 -->
