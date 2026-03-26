# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 주어진 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 색인, GeoJSON, 공간 데이터(행정경계), 일부 LLM 기반 지명 번역.
- **특징**: 사각형→행정구역 변환(대표/상세), 섬 자동 감지 및 방향 기반 대표 표현, GeoJSON 생성·일괄 JSON 변환 및 고성능 대량 처리(convert_many).

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 → 문장 전처리 → Kafka/Opensearch 업로드까지의 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker(Compose), Apache Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 토크나이저), Selenium(스크립트 수집 보조).
- **특징**: 컨테이너 기반 다중 서비스 아키텍처, Spark readStream/writeStream으로 Kafka·OpenSearch 연동, Kiwi 기반 텍스트 전처리(udf/pandas_udf) 및 스트리밍 처리 튜닝(타임아웃 트리거).

## B_project
- **설명**: 알고리즘 연습·코딩 테스트 도구 모음 및 관련 자동화/참고 문서 저장소입니다.
- **기술**: Python 중심(알고리즘 라이브러리, Jupyter Notebook), FastAPI/Async(문서 참조), LLM 유틸리티 모듈.
- **특징**: boj_bible(자료구조·알고리즘 모듈) 구성, CT 자동화 도구 및 kakao_history.ipynb 추가, CT 유틸(common_utils) 기본 LLM 모델을 gpt-5→gpt-5-nano로 변경(명시적 모델 지정 권장).
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
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 34d6f1cd28bbafc0fcdc1899013c99b0addaf26f -->
