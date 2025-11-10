# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely/GeoPandas, STRtree 공간 인덱스, GeoJSON 파일 처리.  
- **특징**: 사각형→행정구역 변환(대표 표현 포함), 좌표→행정구역 매핑 및 경계 조회, 섬 자동 감지 및 GeoJSON 생성·시각화.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집해 문장 전처리 후 Kafka와 OpenSearch로 적재하는 Docker 기반 스트리밍 파이프라인입니다.  
- **기술**: Docker(복수 compose), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Selenium, Kiwipiepy.  
- **특징**: 마운트 폴더 감시→Spark로 Kafka 토픽 생성 및 재가공, OpenSearch 인덱싱과 웹 검색 인터페이스, Kiwi 기반 텍스트 전처리(오탈자·문장분리·불용어).

## B_project
- **설명**: 알고리즘 풀이와 코딩 테스트 준비를 위한 파이썬 라이브러리 및 자동화 도구 모음입니다.  
- **기술**: Python(자료구조·그래프·트리·문자열·고급 알고리즘 구현), 유틸 스크립트 및 자동화 툴.  
- **특징**: boj_bible(스택/큐/그래프/트리/문자열/네트워크플로우 등) 모듈 구성, CT 자동화 도구 포함, LLM 관련 유틸의 기본 모델이 gpt-5→gpt-5-nano로 변경된 업데이트 노트 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 858349ee7aaec17a19b3533b20300d8cf672cab5 -->
