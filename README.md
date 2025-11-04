# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 빠르게 변환하고 GeoJSON으로 시각화하는 툴입니다.
- **기술**: Python, Shapely/STRtree 공간 인덱스, GeoJSON 파일, Spatial 데이터 처리
- **특징**: 사각형→행정구역 변환(고성능 rect2region_fast_v2), 좌표→행정구역/경계 조회, 섬 자동 감지·GeoJSON 생성 및 일괄 변환

## Mini-Pipeline
- **설명**: YouTube 스크립트를 추출해 문장 전처리 후 Kafka·Opensearch로 업로드하는 E2E 스트리밍 파이프라인입니다.
- **기술**: Docker(컨테이너화), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Kiwipiepy, Selenium
- **특징**: 컨테이너 기반의 스트리밍 아키텍처(입력→Spark→Kafka→Opensearch), 전처리(Kiwipiepy+룰베이스) 병렬 처리 및 검색 UI 연동

## B_project
- **설명**: 알고리즘 연습 및 코딩 테스트 자동화·기록을 위한 도구 모음입니다.
- **기술**: Python, 알고리즘 라이브러리(자료구조·그래프·트리·문자열·고급 알고리즘), LLM 유틸리티
- **특징**: boj_bible(문제 풀이용 모듈) 구성, CT 자동화 도구(전처리·기록), LLM 호출 유틸의 기본 모델이 gpt-5-nano로 변경됨
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 32f4f7955d66731a53770251ca226e46720892bb -->
