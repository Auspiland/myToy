# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국/북한의 행정구역(시·도·시군구 등)으로 변환하고 GeoJSON으로 시각화하는 툴입니다.  
- **기술**: Python, Shapely/Geopandas, GeoJSON, STRtree 공간 인덱스 (spatial index), 주요 GIS 데이터 파일 사용.  
- **특징**: 사각형→행정구역/좌표→행정구역 변환, 섬 자동 감지 및 방향 기반 대표 표현 생성, 행정구역 경계 조회·GeoJSON 생성 및 일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka/Opensearch 업로드까지의 Docker 기반 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker / docker-compose, Apache Spark Structured Streaming, Kafka (kRaft), OpenSearch, FastAPI, Kiwipiepy (한국어 전처리).  
- **특징**: 마운트된 폴더 감시→Spark로 Kafka 토픽/Opensearch에 스트리밍 저장, Kiwi 기반 오탈자·문장 분리 처리(F.pandas_udf), 다중 컨테이너 네트워크 구조로 배치 구성.

## B_project
- **설명**: 알고리즘 문제 풀이 모음 및 코딩 테스트 자동화·기록용 도구 모음입니다.  
- **기술**: Python, Jupyter Notebook, 자료구조·그래프·문자열 알고리즘 구현, LLM 연동 유틸(응답/스트리밍 헬퍼).  
- **특징**: boj_bible(자료구조·알고리즘 라이브러리) 제공, CT 자동화 도구(LLM 기본 모델 변경 등 포함) 및 문제 풀이·예제 노트북 제공.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 0737d14b14c305170fec93ceaaf101791e13d601 -->
