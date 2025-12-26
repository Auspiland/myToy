# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 좌표를 대한민국(남한/북한) 행정구역(시/도 등)으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python 기반(Shapely/GeoPandas/STRtree), GeoJSON 입출력, 공간 인덱스 최적화
- **특징**: 사각형→행정구역 변환(대량 처리 지원), 좌표→행정구역 변환 및 경계 조회, 섬 자동 감지·GeoJSON 파일 생성/시각화

## Mini-Pipeline
- **설명**: YouTube 스크립트 수집부터 문장 전처리·Kafka 전송·OpenSearch 적재·검색 UI까지의 E2E 스트리밍 파이프라인입니다.
- **기술**: Docker 컴포즈(컨테이너화), Apache Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy
- **특징**: Streaming 기반 파일 감시→Spark→Kafka→OpenSearch 흐름, 한국어 전처리(Kiwipiepy + 규칙), 컨테이너 네트워크 구성 및 검색 인터페이스 제공

## B_project
- **설명**: 알고리즘/코딩테스트 연습용 라이브러리 및 자동화 도구 모음입니다.
- **기술**: Python(알고리즘 모듈, 노트북), 문제 풀이 유틸리티, LLM 호출 유틸 포함
- **특징**: boj_bible(자료구조·그래프·트리·문자열 등) 모듈화, CT 자동화 및 LLM 관련 유틸 변경 이력, 예제 노트북(문제 풀이 함수) 포함
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

<!-- LAST_PROCESSED_SHA: c3ecbcc8631685f197384593e926f5f3673c7942 -->
