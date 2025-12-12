# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남·북한 포함) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구  
- **기술**: Python, geopandas/shapely, STRtree 공간 인덱스, GeoJSON  
- **특징**: 사각형→행정구역 변환(대표 표현 포함), 섬 자동 감지 및 방향 기반 표현, 경계 조회·GeoJSON 생성·JSON 일괄 변환

## Mini-Pipeline
- **설명**: YouTube URL을 입력으로 받아 문장 전처리 후 Kafka·Opensearch에 업로드하는 스트리밍 E2E 파이프라인  
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Kiwipiepy  
- **특징**: 컨테이너 기반 실시간 파이프라인(파일 모니터→Spark→Kafka→Opensearch), Kiwi 기반 한국어 전처리(udf 병렬화), 웹 검색 연동 및 로그/디버깅용 콘솔 출력

## B_project
- **설명**: 알고리즘 연습·코딩 테스트 도구 모음 및 관련 자동화 유틸리티 모음집  
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열 등), Jupyter 노트북, FastAPI/LLM 유틸(프로젝트 일부)  
- **특징**: boj_bible 알고리즘 라이브러리, CT 자동화·기록 도구(LLM 호출 유틸 포함), kakao_history 노트북 및 운영·개발 가이드 문서(special_prompt.md) 추가 (기본 모델 변경 안내 포함)
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 5ef0c73c9ed4be1bd929238706edd692b9cfb3d4 -->
