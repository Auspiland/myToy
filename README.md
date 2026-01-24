# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 단일 좌표를 대한민국(남·북 포함) 행정구역으로 매핑하고 GeoJSON으로 생성·시각화하는 공간 변환 도구.  
- **기술**: Python, Shapely(STRtree), GeoJSON, pandas, 공간 인덱싱/필터링.  
- **특징**: 사각형→행정구역(대표/상세) 변환·대량 처리, 섬 자동 감지 및 행정구역 경계 조회, GeoJSON 생성 및 시각화/배포 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리, Kafka·Opensearch 업로드까지 동작하는 E2E 스트리밍 파이프라인(컨테이너화).  
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Kiwipiepy.  
- **특징**: 컨테이너 기반 네트워크로 분리된 서비스 구성, streaming 기반 파일 감시→Kafka→Opensearch 흐름, 한국어 전처리(Kiwi + 룰베이스) 및 대규모 처리에 맞춘 운영 설정.

## B_project
- **설명**: 알고리즘/코딩테스트 학습용 라이브러리와 자동화 도구(문제 풀이 모듈, CT 워크플로우, 관련 노트북 및 운영 가이드).  
- **기술**: Python(알고리즘 구현, 스크립트·노트북), FastAPI/Async 관련 도구(문서 참고), LLM 유틸리티 포함.  
- **특징**: boj_bible(자료구조·알고리즘 모듈) 집합, CT 자동화·샘플 문제(노트북 포함), LLM 연동 유틸(기본 모델 파라미터 변경 등) 및 운영/개발 가이드 문서.

## 기타(루트 및 공통 파일)
- **설명**: 모노레포 공통 설정·데이터(예: using_data 경계 파일), 스크립트 및 배포/유틸 문서들을 포함.  
- **기술**: 공통 Python 스크립트, GeoJSON 데이터, GitHub Actions용 메타 정보 등.  
- **특징**: 핵심 경계 데이터(대한민국·북한) 저장, 유틸 스크립트(변환·검증), 자동 업데이트 마커/CI 연동용 메모 지원.
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
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: ca1ec7ff47c3fea620ae5be01f8a4db673f49444 -->
