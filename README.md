# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 한반도(남/북) 행정구역으로 변환하여 대표 텍스트와 경계 정보를 제공하는 도구  
- **기술**: Python, Shapely/STRtree, GeoJSON, pandas 등 공간연산 라이브러리  
- **특징**: 사각형→행정구역 변환(대량 처리 최적화), 섬 자동 감지 및 방향 기반 대표 표현, GeoJSON 생성·시각화 및 경계 조회

## Mini-Pipeline
- **설명**: Youtube 스크립트 수집 후 문장 전처리하여 Kafka·Opensearch로 업로드하는 컨테이너 기반 스트리밍 파이프라인  
- **기술**: Docker, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Kiwipiepy  
- **특징**: 마운트 폴더 감시→Kafka 토픽 전송→Spark로 전처리(오탈자 수정·문장 분리)→Opensearch 색인 및 웹 검색 UI 연동

## B_project
- **설명**: 알고리즘 문제 풀이 및 코딩 테스트 자동화·기록을 위한 파이썬 프로젝트 집합  
- **기술**: Python(자료구조·알고리즘 구현), 유틸 스크립트, LLM 연동 유틸리티  
- **특징**: boj_bible 알고리즘 라이브러리(기본/그래프/트리/문자열 등), CT 자동화 도구 및 LLM 관련 유틸 제공(기본 모델 파라미터 변경 안내)
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: e2563355edc3ef0bccaf940ae1ad83748850ba55 -->
