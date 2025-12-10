# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 출력/시각화하는 도구  
- **기술**: Python, Shapely/STRtree 기반 공간색인, GeoJSON, LLM(지명 번역 보조)  
- **특징**: 사각형/포인트 → 행정구역 변환(대표 표현 포함), GeoJSON 생성·경계/중심점 시각화, 대량 변환·섬 자동 감지 및 성능 최적화

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·Spark·Opensearch 업로드까지의 E2E 스트리밍 파이프라인  
- **기술**: Docker Compose, Kafka(kRaft), Spark Structured Streaming, OpenSearch, FastAPI/Nginx, Selenium/Kiwipiepy  
- **특징**: Streaming 기반 데이터 흐름(Kafka↔Spark↔Opensearch), 컨테이너화된 네트워크 구성(Nginx→FastAPI 라우팅), Kiwipiepy+pandas_udf를 이용한 한글 전처리 및 파이프라인 자동화

## B_project
- **설명**: 알고리즘 문제 풀이와 코딩 테스트 자동화 도구를 모아둔 레포지토리  
- **기술**: Python, Jupyter Notebook, FastAPI/Async(문서화된 가이드), LLM 유틸 함수  
- **특징**: BOJ용 알고리즘 라이브러리(자료구조/그래프/트리/문자열/고급 알고리즘), CT 자동화·LLM 헬퍼(기본 모델 gpt-5-nano 변경 안내), 문제 풀이 노트북(kakao_history.ipynb) 예제 포함
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 0b658d845304373156d8a57d05a39dfd8975dd90 -->
