# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역 단위로 변환하고 GeoJSON으로 시각화하는 도구  
- **기술**: Python, shapely/geopandas 기반 공간색인(STRtree), GeoJSON 처리  
- **특징**: 사각형·좌표 → 행정구역 변환(대표문구 포함), 섬 자동 감지 및 행정경계 조회·GeoJSON 생성, 대량 처리용 최적화(rect2region_fast_v2)

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 → 문장 전처리 → Kafka/Spark → Opensearch로 업로드하는 E2E 스트리밍 파이프라인  
- **기술**: Docker Compose, Apache Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy  
- **특징**: 컨테이너 기반 다중 서비스 스트리밍 아키텍처, Spark로 파일 감시→토픽/인덱스 삽입(유효성/디버깅용 writeStream), 한국어 전처리(UDF/Kiwi) 및 검색 인터페이스 연동

## B_project
- **설명**: 알고리즘 문제 풀이와 코딩 테스트 자동화·도움 도구 모음  
- **기술**: Python 중심(알고리즘 라이브러리, Jupyter 노트북), 일부 LLM 연동 유틸리티 및 배포 가이드 문서  
- **특징**: boj_bible(자료구조·그래프·트리·문자열 등) 모듈, CT 자동화 도구 및 LLM 헬퍼(response_GPT 등, 기본 모델 gpt-5-nano), 예제 노트북(문제 풀이) 및 운영·배포 가이드 문서
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

<!-- LAST_PROCESSED_SHA: 37362eceabd70fc0d7a39ce02c5d51da7822e3ab -->
