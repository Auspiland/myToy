# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 공간 변환 도구
- **기술**: Python, Shapely/STRtree 기반 공간 색인, GeoJSON, (행정경계) GeoJSON 데이터
- **특징**: 사각형→시/도/군·구 변환 및 대표 문구 생성, 섬 자동 감지/면적 기반 표현, 경계 조회·GeoJSON 생성/일괄 변환

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·Kafka·Spark를 거쳐 Opensearch에 업로드하는 E2E 스트리밍 파이프라인
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Selenium, Kiwipiepy
- **특징**: 컨테이너화된 스트리밍 파이프라인(파일→Kafka→Spark→Opensearch), 한국어 전처리(오탈자/문장분리) 및 검색 연동, 네트워크/서비스 분리 구성

## B_project
- **설명**: 알고리즘 연습 및 코딩 테스트 자동화·도구 모음(라이브러리·노트북·운영 가이드 포함)
- **기술**: Python (알고리즘 모듈/노트북), Jupyter, FastAPI/DB/Redis(운영 가이드 문서), LLM 유틸리티
- **특징**: 백준용 알고리즘 라이브러리(자료구조·그래프·트리·문자열 등), CT 자동화·LLM 호출 유틸 변경 사항 및 예제·노트북 추가, 운영·배포 가이드 문서화
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: d632a92560198ed33e54c0623312a9f7ebcc0f4c -->
