# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 입력된 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역 단위로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, shapely/STRtree 기반 공간 인덱싱, GeoJSON 처리, pandas, GitHub 연동 스크립트.
- **특징**: 고성능 사각형→행정구역 변환(rect2region_fast_v2), 섬 자동 감지 및 대표 텍스트 생성, 행정경계 조회·GeoJSON 생성·파일 일괄 변환 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리, Kafka와 Opensearch로의 업로드까지의 컨테이너화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker/Docker-Compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Kiwipiepy(한국어 전처리).
- **특징**: 멀티 컨테이너 네트워크 아키텍처(Nginx→FastAPI), Spark readStream/writeStream 기반 데이터 흐름, Kiwi+pandas_udf를 이용한 한국어 오탈자·문장 분리 전처리.

## B_project
- **설명**: 알고리즘 문제 풀이용 라이브러리 및 코딩 테스트 자동화·기록 도구 모음입니다.
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열 등), Jupyter 노트북, FastAPI/운영 가이드 문서 등.
- **특징**: boj_bible(기초·그래프·트리·문자열·고급 알고리즘) 구성, CT 자동화용 유틸과 LLM 헬퍼(기본 모델이 gpt-5→gpt-5-nano로 변경) 포함, kakao_history.ipynb 및 운영·배포 가이드 문서 제공.
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

<!-- LAST_PROCESSED_SHA: b0d01b72ae55b7de1f480d1427c4eb74e40a3ed3 -->
