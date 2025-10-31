# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 한반도 행정구역(광역·기초단위)으로 변환하고 GeoJSON으로 생성·시각화합니다.
- **기술**: Python, shapely/STRtree 기반 공간 인덱스, GeoJSON
- **특징**: 사각형→행정구역 변환(대표 문구 옵션), 경계 정보 조회 및 GeoJSON 생성/시각화, 섬 자동 감지·대량 JSON 변환

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·Opensearch 업로드까지의 도커 기반 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy
- **특징**: 파일 감시 → Spark로 Kafka 토픽 전송 및 Opensearch 색인, Kiwipiepy 기반 문장 전처리(pandas_udf 병렬 처리), docker-compose로 서비스/네트워크 분리

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트(백준) 문제 풀이를 위한 라이브러리 및 도구 모음입니다.
- **기술**: Python
- **특징**: boj_bible(기본 자료구조, 그래프, 트리, 문자열, 고급 알고리즘) 모듈 제공, CT(코딩 테스트 자동화·기록) 도구 포함
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 9bbd585f6315a6d88d8c03c155fa3c840cd887d1 -->
