# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON을 생성·시각화하는 도구입니다.
- **기술**: Python, Shapely/GEOS, STRtree 공간 색인, GeoJSON, pandas, (LLM 기반 지명 번역), GitHub 연동.
- **특징**: 사각형→행정구역 대량 변환(성능 최적화된 rect2region_fast_v2), 섬 자동 감지 및 방향 기반 대표 표현, 행정구역 경계 조회·GeoJSON 생성 및 시각화.

## Mini-Pipeline
- **설명**: YouTube 스크립트 수집부터 전처리(Kiwi)·Kafka·Spark·Opensearch로 업로드하는 컨테이너화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker Compose, Apache Spark(Structured Streaming), Kafka(kRaft), Opensearch, FastAPI, Nginx, Selenium, Kiwipiepy.
- **특징**: 컨테이너별 모듈화된 네트워크 구성(Shared-net), Spark+Kafka 기반 스트리밍 처리·전처리(pandas_udf 사용), Opensearch 인덱싱 및 웹 검색 연동.

## B_project
- **설명**: 알고리즘 및 코딩 테스트 문제 풀이용 라이브러리·예제·도구 모음입니다.
- **기술**: Python, Jupyter Notebook, 자료구조·알고리즘 구현(그래프/트리/문자열 등), CT 자동화 유틸(LLM 연동 문서 포함).
- **특징**: boj_bible(기본 자료구조·알고리즘 모음), CT 자동화·LLM 호출 유틸(기본 모델 변경 안내 포함), 노트북 기반 문제 풀이 예제 및 재사용 가능 코드 제공.
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

<!-- LAST_PROCESSED_SHA: 66e99b9f85b12adc94b1dc0695895e61ecdb67bd -->
