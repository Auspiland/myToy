# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표나 사각형 영역을 대한민국/북한 행정구역으로 변환하고 관련 GeoJSON을 생성·시각화하는 도구  
- **기술**: Python, Shapely(STRtree) 기반 공간 인덱싱, GeoJSON, 공간 데이터(행정구역) 파일  
- **특징**: 사각형→행정구역 고속 변환(rect2region_fast_v2), 섬 지역 자동 감지·방향 기반 대표표현, 경계 조회·GeoJSON 생성 및 JSON 일괄 변환

## Mini-Pipeline
- **설명**: 유튜브 스크립트 추출부터 문장 전처리·Kafka/Opensearch 업로드까지 동작하는 스트리밍 E2E 파이프라인  
- **기술**: Docker(Compose), Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy, Selenium(수집 보조)  
- **특징**: 폴더 모니터링→Spark로 Kafka 토픽 생성·가공, Kafka 기반 파이프라인 연동 및 Opensearch 색인·검색, 컨테이너 기반 분산 아키텍처

## B_project
- **설명**: 알고리즘 연습·코딩테스트용 유틸과 자동화 도구들을 모아놓은 프로젝트  
- **기술**: Python(알고리즘/유틸 모듈), Jupyter 노트북, FastAPI/LLM 연동 유틸(프로젝트 일부)  
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT 자동화·LLM 헬퍼(response_GPT 계열 함수) 포함 및 기본 모델 변경 알림, 문제 풀이 예제 노트북(코드 재사용 가능)
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 8ae1d35023be434781345ef1b36fd206118bf055 -->
