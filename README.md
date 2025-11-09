# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 좌표를 대한민국 행정구역(광역/시군구 등)으로 변환하고 GeoJSON으로 시각화하는 도구.
- **기술**: Python, shapely/geopandas, STRtree 공간 색인, GeoJSON, pyproj.
- **특징**: 사각형→행정구역 변환(대량 처리 최적화), 좌표→행정구역 매핑, 섬 자동 감지 및 GeoJSON 생성/조회.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 후 문장 전처리하여 Kafka/Spark/Opensearch로 업로드하는 컨테이너 기반 스트리밍 파이프라인.
- **기술**: Docker, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Selenium, Kiwipiepy.
- **특징**: 전체 E2E 컨테이너화(Streaming 모드), Spark↔Kafka↔Opensearch 연동 파이프라인, 한국어 전처리(Kiwipiepy) 및 검색 UI 연동.

## B_project
- **설명**: 알고리즘 학습과 코딩 테스트 자동화용 라이브러리 및 도구 모음.
- **기술**: Python 기반 알고리즘/자료구조 구현(그래프·트리·문자열 등), 자동화 스크립트, LLM 연동 유틸리티.
- **특징**: BOJ 문제 풀이용 모듈 집합, 코딩 테스트 자동화(CT) 도구, LLM 관련 기본 모델(gpt-5 → gpt-5-nano) 설정 변경 안내.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 01c229996734122aa76cd1f3f480fc21c49864f8 -->
