# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남북 포함) 행정구역으로 변환하고 GeoJSON으로 시각화하는 파이썬 툴입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간 인덱스, GeoJSON, GitHub Actions.  
- **특징**: 사각형→행정구역 변환(대량 처리 최적화), 섬 자동 감지 및 대표 표현 생성, 경계 조회 및 GeoJSON 파일 생성/시각화.

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트를 추출해 전처리 후 Kafka와 OpenSearch로 스트리밍 업로드하는 컨테이너화된 E2E 파이프라인입니다.  
- **기술**: Docker Compose, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI/Nginx.  
- **특징**: 스트리밍 기반 파이프라인(파일 감시→Kafka 토픽→가공→Opensearch), Kiwipiepy 기반 한국어 전처리(pandas_udf 사용), 네트워크 분리 및 컨테이너별 구성 최적화.

## B_project
- **설명**: 알고리즘 연습 및 코딩 테스트 자동화 도구 모음과 관련 문서·노트북을 포함한 프로젝트입니다.  
- **기술**: Python, Jupyter Notebook, 알고리즘 라이브러리 구성(자료구조·그래프·문자열 등), FastAPI/비동기 관련 가이드 문서(참고).  
- **특징**: boj_bible 알고리즘 모듈(기본/그래프/트리/문자열 등), CT 자동화 및 LLM 헬퍼 유틸(기본 모델이 gpt-5→gpt-5-nano로 변경 안내 포함), 문제 풀이용 노트북 및 샘플 함수 제공.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 3fe296d2ce41f1db8d039778363b2df99b9740db -->
