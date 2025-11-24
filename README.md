# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 개별 좌표를 대한민국 행정구역(시/도/시군구 등)으로 빠르게 변환하고 시각화하는 도구입니다.  
- **기술**: Python, Shapely/STRtree 공간 인덱스, GeoJSON 처리, GitHub push/파일 I/O.  
- **특징**: 고성능 rect2region_fast_v2 기반 사각형→행정구역 변환(일괄 변환 지원), 섬 자동 감지 및 대표 텍스트 생성, 행정구역 경계 조회 및 GeoJSON 생성/시각화.

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트 추출 후 문장 전처리하여 Kafka/Opensearch에 업로드하는 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker(다중 compose), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy, Selenium(수집 보조).  
- **특징**: 컨테이너 기반 다중 네트워크 아키텍처(실시간 스트리밍), Spark→Kafka→OpenSearch 흐름으로 연속 처리, 한국어 전처리(오탈자 보정·문장분리 등) 및 웹 검색 인터페이스 연동.

## B_project
- **설명**: 알고리즘 학습·코딩 테스트 풀이용 라이브러리와 관련 도구 모음입니다.  
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열·고급 알고리즘), Jupyter 노트북, FastAPI/DevOps 문서(참고).  
- **특징**: boj_bible(기초/그래프/트리/문자열/고급) 모듈 제공, 코딩 테스트 자동화·기록 도구(LLM 호출 유틸 포함, 기본 모델 gpt-5-nano 변경 안내), 예제 노트북(kakao_history) 및 운영·배포 가이드 문서 제공.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 0ae09f600901c2093587d8c7efb3b0928619bf61 -->
