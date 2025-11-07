# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역 단위로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/GeoPandas, STRtree 공간 인덱스, GeoJSON
- **특징**: 사각형→행정구역·좌표→행정구역 변환, 섬 자동 감지(지역 방향/비율 기반), GeoJSON 생성·경계 조회 및 일괄 변환

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·Opensearch 업로드까지 수행하는 컨테이너 기반 스트리밍 파이프라인입니다.
- **기술**: Docker, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, Kiwipiepy, Nginx/FastAPI
- **특징**: 파일 드롭 기반 스트리밍 수집 및 Kafka 토픽 처리, Spark에서 Kiwipiepy로 텍스트 전처리(오탈자·문장 분리), OpenSearch 색인 및 웹 검색 연동

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트 자동화·기록을 위한 도구 모음입니다.
- **기술**: Python 중심 라이브러리(알고리즘 구현), LLM 연동 유틸리티
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT(코딩 테스트) 자동화 도구 및 LLM 호출 유틸(기본 모델 설정 변경 내역 포함)
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: e71f194dd18042f857a204074c1a30717f5b5479 -->
