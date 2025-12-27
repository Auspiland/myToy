# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## [geo_map]
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역 명칭으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON, (Geo)boundary 데이터 처리.
- **특징**: 사각형→행정구역 변환(대·소단위), 좌표→행정구역 매핑 및 섬 자동 감지, 경계 조회·GeoJSON 생성 및 일괄 변환.

## [Mini-Pipeline]
- **설명**: YouTube URL로부터 스크립트를 추출해 문장 전처리 후 Kafka·Opensearch로 업로드하는 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker-compose, Kafka(kRaft), Spark Structured Streaming, OpenSearch, FastAPI/Nginx, Selenium, Kiwipiepy.
- **특징**: 컨테이너 기반 스트리밍 파이프라인(파일→Kafka→Spark→Opensearch), Kiwi 기반 한국어 전처리(pandas_udf 사용), 웹 검색 인터페이스 연동.

## [B_project]
- **설명**: 알고리즘 문제 풀이·코딩테스트 지원 라이브러리 및 관련 도구 모음입니다.
- **기술**: Python (모듈화된 알고리즘 라이브러리), Jupyter 노트북, LLM 유틸(백엔드 호출 래퍼).
- **특징**: boj_bible(자료구조·그래프·문자열 등) 모듈, CT 자동화·LLM 호출 유틸(기본 모델 업데이트 포함), 문제 풀이용 노트북·참고문서 제공.
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

<!-- LAST_PROCESSED_SHA: 9924b2cd5e2c7635e4c95c1a8ccd636152c5cc53 -->
