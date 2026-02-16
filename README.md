# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표나 사각형 영역을 대한민국·북한의 행정구역(시/도/시군구 등)으로 변환하는 도구입니다.
- **기술**: Python, Shapely/GeoJSON 기반 공간처리(STRtree 인덱스), GeoJSON 입출력
- **특징**: 고성능 rect2region_fast_v2 기반 영역→행정구역 변환, 섬 지역 자동 감지 및 대표 표현 규칙 적용, 경계 조회·GeoJSON 생성 및 시각화·배치 변환 지원

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트 추출 후 전처리하여 Kafka와 OpenSearch에 업로드하는 E2E 스트리밍 파이프라인입니다.
- **기술**: Docker/Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리)
- **특징**: 마운트된 폴더 감시 → Spark readStream으로 Kafka/Opensearch 저장, Kiwipiepy+룰베이스 기반 문장 전처리(udf/pandas_udf 사용), 멀티컨테이너 아키텍처(Nginx 게이트웨이 포함)

## B_project
- **설명**: 알고리즘 학습·코딩 테스트용 라이브러리 및 자동화 도구 모음입니다.
- **기술**: Python 중심(모듈화된 알고리즘 패키지, Jupyter 노트북), LLM 호출 유틸리티(공통 유틸)
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급알고리즘) 모듈 제공, CT(코딩테스트) 자동화·기록 도구와 LLM 래퍼(기본 모델 gpt-5-nano로 변경) 포함, kakao_history.ipynb 등 실전 문제 풀이 예제 제공
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

<!-- LAST_PROCESSED_SHA: 8365edb82d6fa61eeb018b15fb1374036e14eb81 -->
