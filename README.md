# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 개별 좌표를 대한민국(남한/북한) 행정구역으로 변환해주는 지리 공간 변환 도구
- **기술**: Python, Shapely/GeoPandas 기반 공간 인덱스(STRtree), GeoJSON 입출력
- **특징**: 고성능 사각형→행정구역 변환(rect2region_fast_v2), 좌표→행정구역 및 경계 정보 조회, GeoJSON 생성·시각화 및 섬 자동 감지

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·카프카·오픈서치 업로드까지의 스트리밍 E2E 파이프라인
- **기술**: Docker / docker-compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI + Nginx, Kiwipiepy(문장 전처리)
- **특징**: 컨테이너 기반 네트워크로 구성된 스트리밍 파이프라인, Spark→Kafka→OpenSearch 연동 및 실시간 전처리(토큰화·오탈자 수정 등), Web 검색 인터페이스 연동

## B_project
- **설명**: 알고리즘 문제 풀이 및 코딩 테스트 지원을 위한 유틸·솔루션 모음
- **기술**: Python 중심(알고리즘 라이브러리, Jupyter 노트북), FastAPI/DB/Redis 관련 운영문서 참고 자료
- **특징**: boj_bible(자료구조·그래프·문자열·고급 알고리즘) 모듈화, CT 자동화·문서화 도구 및 예제 노트북(kakao_history), LLM 호출 유틸의 기본 모델 변경 등 운영·사용 가이드 포함
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 4a55778c507dd299f4efe4a854694823237207bc -->
