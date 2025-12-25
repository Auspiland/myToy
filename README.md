# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 경계·중심정보를 제공하는 공간 변환 도구입니다.  
- **기술**: Python, shapely/STRtree 기반 공간 인덱스, GeoJSON (입출력), pandas/기본 유틸 스크립트.  
- **특징**: 사각형→행정구역 및 좌표→행정구역 변환(대량 처리 지원), 섬 자동 감지 및 방향 기반 대표 표현 생성, 행정구역 경계 조회 및 GeoJSON 생성/시각화/일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출을 시작으로 문장 전처리 후 Kafka와 OpenSearch로 업로드하는 컨테이너화된 E2E 스트리밍 파이프라인입니다.  
- **기술**: Docker / docker-compose, Spark Structured Streaming, Kafka (kRaft), OpenSearch, FastAPI + Nginx, Kiwipiepy(한국어 전처리).  
- **특징**: 마운트 폴더 기반 입력 → Spark로 스트리밍 처리 → Kafka 토픽/Opensearch 색인, 컨테이너별 네트워크 분리 및 Nginx 기반 라우팅, 전처리(오탈자·문장분리 등)를 위한 UDF/병렬 처리 구성.

## B_project
- **설명**: 알고리즘 학습·코딩테스트 해결을 위한 라이브러리 및 자동화 도구 모음입니다.  
- **기술**: Python 기반 알고리즘 모듈, Jupyter 노트북, FastAPI/비동기 유틸(문서 참조).  
- **특징**: boj_bible(자료구조·그래프·문자열·트리 등) 알고리즘 모듈, CT 자동화 및 LLM 헬퍼 함수(기본 모델 변경 관련 안내 포함), 문제 풀이용 노트북 및 프로젝트 운영·배포 가이드 문서 제공.
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

<!-- LAST_PROCESSED_SHA: dc3ec0d23a76fdd5c6a6f2227a690e31660fb204 -->
