# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 매핑하고 GeoJSON을 생성/시각화하는 도구입니다.
- **기술**: Python (shapely/pyproj/GeoJSON), STRtree 공간 인덱스, geopandas/pandas 기반 처리.
- **특징**: 최적화된 Rect2Region으로 사각형→행정구역 변환; 섬 자동 감지 및 대표 표현 규칙 적용; 경계 조회·GeoJSON 생성 및 일괄 변환 지원.

## Mini-Pipeline
- **설명**: Youtube 스크립트 추출부터 문장 전처리·Kafka 전송·OpenSearch 업로드까지의 Docker 기반 스트리밍 파이프라인입니다.
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI + Nginx, kiwipiepy(형태소 처리).
- **특징**: Spark로 파일 감시→Kafka 토픽·Opensearch에 writeStream 처리; Kiwi 기반 오탈자 수정·문장 분리 등 전처리(pandas_udf 활용); 컨테이너 네트워크 설계 및 모니터링/디버깅 지원.

## B_project
- **설명**: 알고리즘 연습·코딩테스트 보조 도구 모음(풀이 라이브러리·자동화·참고 문서).
- **기술**: Python 기반 알고리즘 모듈, Jupyter 노트북, FastAPI/Async 관련 운영 가이드 및 LLM 연동 유틸리티.
- **특징**: boj_bible(자료구조·그래프·문자열 등 알고리즘 모듈); CT 자동화 도구 및 LLM 호출 유틸(기본 모델 변경 안내 포함); 문제 풀이 예제(노트북) 및 운영·배포 가이드 문서 제공.
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

<!-- LAST_PROCESSED_SHA: 80eaf8439ec45180f3750362f6f99fcad7bbece5 -->
