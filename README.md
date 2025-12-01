# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 빠르게 변환하고 GeoJSON으로 출력하는 도구  
- **기술**: Python, Shapely/GEOS (STRtree 기반 공간색인), GeoJSON 데이터, 공간 연산 최적화(rect2region_fast_v2)  
- **특징**: 사각형→행정구역 변환(대량 처리 지원), 좌표→행정구역 변환 및 경계 조회, 섬 자동 감지 및 GeoJSON 생성/시각화

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·OpenSearch 업로드까지의 컨테이너화된 스트리밍 E2E 파이프라인  
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy  
- **특징**: Streaming 기반 파이프라인(Spark readStream → Kafka → OpenSearch), 텍스트 전처리(Kiwipiepy + 룰베이스), 웹 UI 연동(Nginx → FastAPI) 및 멀티컨테이너 네트워크 구성

## B_project
- **설명**: 알고리즘/코딩테스트 연습용 라이브러리 및 자동화·기록 도구 모음  
- **기술**: Python(알고리즘 모듈/노트북), Jupyter, LLM 유틸리티(응답 래퍼)  
- **특징**: boj_bible(자료구조·그래프·문자열·고급 알고리즘) 모듈, CT 자동화 및 LLM 기본모델 변경(gpt-5 → gpt-5-nano) 안내, 문제 풀이용 노트북·실습 코드 포함
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 029436607926b8680a07c942341ddfa1c7b3f238 -->
