# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 출력·시각화합니다.
- **기술**: Python, Shapely/STRtree 공간 인덱스, GeoJSON, Pandas (경계 데이터 및 LLM 유틸 포함).
- **특징**: 사각형→행정구역 고속 변환(대량 처리), 섬 자동 감지·대표 표현 규칙, 행정구역 경계 조회 및 GeoJSON 생성/시각화.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·Opensearch 업로드까지의 컨테이너 기반 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker(멀티컨테이너), Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy(형태소 분석).
- **특징**: Spark로 마운트 폴더 감시→Kafka/Opensearch 연계 스트리밍 처리, Kiwipiepy·pandas_udf 기반 전처리, 컨테이너 네트워크·웹 인터페이스 구성.

## B_project
- **설명**: 알고리즘 문제 풀이 및 코딩 테스트 자동화·기록을 위한 도구 모음입니다.
- **기술**: Python 기반 자료구조·알고리즘 구현, 자동화 스크립트, LLM 연동 유틸리티.
- **특징**: boj_bible(기본/그래프/트리/문자열/고급 알고리즘 모듈), CT 자동화·기록 도구, LLM 관련 유틸 기본 모델 파라미터(gpt-5→gpt-5-nano) 안내.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 970364498c9024d656223ed2a630b3144d065e22 -->
