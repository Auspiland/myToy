# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 좌표를 한반도 행정구역(시/도/시군구 등)으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/STRtree, GeoPandas, GeoJSON, 공간 인덱싱(Spatial Index).
- **특징**: 사각형→행정구역/좌표→행정구역 변환, 섬 자동 감지 및 대표 문구 생성, GeoJSON 생성·일괄 변환 및 경계 조회 기능.

## Mini-Pipeline
- **설명**: Youtube 스크립트 추출부터 문장 전처리, Kafka/Spark를 통한 스트리밍 처리 및 Opensearch 업로드까지의 E2E 파이프라인입니다.
- **기술**: Docker(Compose), Apache Kafka(kRaft), Apache Spark(Structured Streaming), Opensearch, FastAPI, Nginx, Kiwipiepy.
- **특징**: 컨테이너 기반 스트리밍 아키텍처, Spark로 Kafka/Opensearch 연동·실시간 처리, 한국어 전처리(키위) 및 웹 검색 인터페이스 연동.

## B_project
- **설명**: 알고리즘 학습과 코딩 테스트 준비를 위한 문제 풀이 및 라이브러리 모음입니다.
- **기술**: Python 기반 알고리즘 구현 및 유틸 스크립트.
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘 모듈), 코딩 테스트 자동화·기록 도구(CT).
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 466e3151945113a4d42dfb69df6f2b530175ea88 -->
