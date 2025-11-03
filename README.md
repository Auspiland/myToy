# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 출력·시각화합니다.
- **기술**: Python, geopandas/shapely, STRtree 공간 인덱싱, GeoJSON
- **특징**: 사각형→행정구역 고속 변환(배치 지원), 섬 자동 감지 및 대표 텍스트 규칙, 경계 조회·GeoJSON 생성

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·Kafka·Opensearch 업로드까지 동작하는 E2E 스트리밍 파이프라인입니다.
- **기술**: Docker(다중 컨테이너), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy
- **특징**: Spark→Kafka→Opensearch 기반 실시간 처리, 도커 컴포즈로 구성된 컨테이너 네트워크, Kiwipiepy+Pandas UDF를 이용한 한글 전처리(및 Selenium 기반 수집 보조)

## B_project
- **설명**: 알고리즘 문제 풀이와 코딩 테스트 자동화 도구를 모아둔 프로젝트입니다.
- **기술**: Python 기반 알고리즘 라이브러리 및 유틸, LLM 호출 유틸리티
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT(자동화·기록) 도구, LLM 관련 유틸(기본 모델 파라미터 변경 안내: gpt-5 → gpt-5-nano)
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: bc3971f8552d5d227c888e51ee3a125600594748 -->
