# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 단일 좌표를 대한민국(남한/북한) 행정구역으로 매핑하고 GeoJSON으로 내보내는 도구입니다.
- **기술**: Python, GeoJSON, Shapely(STRtree 기반 공간 인덱스), 지역 경계 GeoJSON 데이터
- **특징**: 사각형→행정구역 변환(고성능 rect2region_fast_v2), 섬 자동 감지 및 방향 기반 대표 표현, GeoJSON 생성·시각화 및 일괄 JSON 변환

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트 추출→전처리→Kafka·Opensearch로 업로드하는 Docker 기반 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker, Apache Spark 스트리밍, Kafka(kRaft), OpenSearch, FastAPI + Nginx, Kiwipiepy(한글 전처리)
- **특징**: mount 폴더 감시 기반 Spark readStream→Kafka 토픽 파이프라인, Kiwipiepy+pandas_udf를 이용한 문장 전처리·오탈자 수정, OpenSearch 기반 검색 및 웹 노출

## B_project
- **설명**: 알고리즘 학습·코딩 테스트용 라이브러리와 자동화 도구들을 모아둔 저장소입니다.
- **기술**: Python(알고리즘 모듈, Jupyter 노트북), 문제 풀이 유틸리티, LLM 연동 유틸
- **특징**: boj_bible(자료구조·그래프·문자열·고급 알고리즘) 모듈, CT 자동화·기록용 도구(LLM 호출 유틸 포함, 기본 모델 gpt-5-nano 변경 안내), 예제 노트북(kakao_history) 및 운영·배포 가이드 문서
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 298685cc2caca5defec94e88a4b1d6ad68baf53d -->
