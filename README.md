# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국 행정구역(광역/기초단위)으로 변환하고 GeoJSON으로 시각화하는 Python 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간색인, GeoJSON, 경계 데이터(국내/북한), pandas 등.  
- **특징**: 사각형→행정구역 변환(단일/다중 처리), 좌표→행정구역 매핑·섬 자동 감지, GeoJSON 생성 및 배치 JSON 변환·경계 조회.

## Mini-Pipeline
- **설명**: YouTube URL에서 스크립트를 추출해 문장 전처리 후 Kafka와 OpenSearch로 업로드하는 컨테이너형 스트리밍 파이프라인입니다.  
- **기술**: Docker/Docker Compose, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리).  
- **특징**: Spark readStream/writeStream 기반 E2E 스트리밍 처리, 컨테이너별 네트워크 분리·역방향 프록시 구성, Kiwipiepy + pandas_udf를 이용한 대량 텍스트 전처리.

## B_project
- **설명**: 알고리즘 문제 풀이(백준)와 코딩 테스트 자동화/기록을 위한 파이썬 도구 모음입니다.  
- **기술**: Python(모듈화된 알고리즘 라이브러리), Jupyter 노트북, FastAPI·LLM 연동 유틸(선택적).  
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 구성, CT 자동화 도구 및 노트북 수록, LLM 관련 유틸(기본 모델 변경 안내 포함).
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 4e024877c010c7a25fd0ff58eb98a079532fd2ff -->
