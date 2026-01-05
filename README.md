# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/GeoPandas 기반 공간 인덱스(STRtree), GeoJSON 처리.
- **특징**: 사각형→행정구역 변환(최적화된 rect2region_fast_v2), 좌표→행정구역 변환 및 경계 조회, 섬 자동 감지·GeoJSON 생성 및 배치 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·Opensearch 업로드까지의 Docker 기반 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker/ docker-compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy.
- **특징**: Spark+Kafka를 통한 실시간 파이프라인(토픽 기반 처리 및 Opensearch 적재), Kiwipiepy 기반 한국어 전처리(pandas_udf 적용), 컨테이너 네트워크 분리 및 nginx→fastapi 라우팅 구성.

## B_project
- **설명**: 알고리즘 풀이용 라이브러리와 코딩 테스트 자동화·기록 도구 모음입니다.
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열 등), Jupyter 노트북, FastAPI/LLM 유틸(프로젝트 내 도구).
- **특징**: boj_bible로 정리된 알고리즘·자료구조 모듈, CT 자동화용 전처리·LLM 호출 유틸(기본 모델 gpt-5-nano로 변경 관련 안내 포함), 재사용 가능한 문제 풀이 노트북 및 운영·배포 가이드 문서.
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

<!-- LAST_PROCESSED_SHA: dc95eff097b34f7a22db1f8e0e15274b3df6aba0 -->
