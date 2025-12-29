# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 좌표를 대한민국(남한/북한) 행정구역(시/도/구군 등)으로 변환하고 GeoJSON으로 출력하는 도구입니다.
- **기술**: Python (Shapely/STRtree 기반 공간 색인), GeoJSON, geopandas/로컬 경계 데이터, GitHub 연동
- **특징**: 사각형→행정구역 변환(대량 처리 지원), 섬 자동 감지 및 방향 기반 대표표현, 행정구역 경계 조회·GeoJSON 생성

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·Opensearch 업로드까지의 컨테이너화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose 기반 컨테이너( Spark, Kafka(kRaft), FastAPI, Nginx, Opensearch ), Selenium, Kiwipiepy(한국어 전처리)
- **특징**: Spark Streaming ↔ Kafka 토픽 파이프라인, 전처리(오탈자·문장분리·불용어) 및 Opensearch 인덱싱, 웹 UI 연동(Nginx + FastAPI)

## B_project
- **설명**: 알고리즘/코딩테스트 연습과 자동화 도구를 모아둔 저장소입니다.
- **기술**: Python 기반 알고리즘 라이브러리 및 노트북(.ipynb), FastAPI/DB/DevOps 가이드 문서(운영·배포 관련)
- **특징**: boj_bible 알고리즘 모듈(자료구조·그래프·트리·문자열 등), CT 자동화·기록 도구 및 LLM 유틸(기본 모델 변경 안내), 문제 풀이용 예제 노트북 추가
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

<!-- LAST_PROCESSED_SHA: 9e6ab6a63fb6cc9542e46a07308e52fbc20ff7e1 -->
