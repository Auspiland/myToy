# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 단일 좌표를 대한민국(남한/북한) 행정구역(시/도 등)으로 매핑하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, GeoJSON, Shapely/pyproj (STRtree spatial index), 지역 경계 데이터(GeoJSON), GitHub 연동 스크립트.  
- **특징**: 고성능 Rect→Region 변환(STRtree 기반, rect2region_fast_v2), 섬 자동 감지 및 대표 텍스트 규칙, GeoJSON 생성·시각화 및 대량(파일) 변환 지원.

## Mini-Pipeline
- **설명**: 유튜브 URL을 입력으로 받아 문장 전처리 후 Kafka와 OpenSearch로 업로드하는 컨테이너 기반 E2E 스트리밍 파이프라인입니다.  
- **기술**: Docker Compose(다중 네트워크), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI + Nginx, Selenium(스크립트 수집), Kiwipiepy.  
- **특징**: Spark readStream→Kafka→Opensearch 흐름의 실시간 처리 파이프라인, 컨테이너 간 네트워크 구성(서비스 분리), 한국어 전처리(오탈자 수정·문장 분리·불용어 처리) 및 대용량 스트리밍 최적화.

## B_project
- **설명**: 알고리즘 연습 및 코딩 테스트 자동화·도구 모음(라이브러리, 문제 풀이 유틸, 참고 노트 등)입니다.  
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열·고급 알고리즘), FastAPI/Async 관련 운영 문서(가이드), 노트북(.ipynb) 및 유틸 스크립트.  
- **특징**: boj_bible 형태의 알고리즘 라이브러리(기본·그래프·트리·문자열·고급), CT(코딩 테스트) 자동화 도구와 LLM 호출 유틸(기본 모델 변경: gpt-5 → gpt-5-nano), 문제 풀이 노트북 및 운영/배포 가이드 문서 포함.
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
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: dcb808da43743f39dc149cc1ad0c232458fd916e -->
