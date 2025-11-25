# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국 행정구역(시/도/시군구 등)으로 변환하고 경계·대표 텍스트·GeoJSON을 생성하는 도구
- **기술**: Python, Shapely/STRtree 기반 공간 인덱스, GeoJSON 처리
- **특징**: 사각형→행정구역(대량 처리 최적화), 좌표→행정구역 변환 및 경계 조회, GeoJSON 생성·시각화·섬 자동 감지

## Mini-Pipeline
- **설명**: YouTube URL에서 스크립트 추출 후 문장 전처리하여 Kafka와 Opensearch에 업로드하는 컨테이너 기반 E2E 스트리밍 파이프라인
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Kiwipiepy
- **특징**: 전체 컨테이너 아키텍처(Nginx→FastAPI→Spark), Spark로 Kafka/Opensearch 연동 및 스트리밍 처리, Kiwipiepy·pandas_udf 기반 한국어 전처리(오탈자·분문·불용어)

## B_project
- **설명**: 알고리즘 문제 풀이 및 코딩 테스트용 라이브러리·도구 모음 레포지토리
- **기술**: Python 기반 알고리즘 모듈·노트북, (참고용) FastAPI/Async 운영 가이드 문서
- **특징**: boj_bible(자료구조·그래프·문자열·고급 알고리즘) 모듈, CT 자동화·예제 노트북(문제 풀이 함수 포함), LLM 유틸 기본 모델이 'gpt-5-nano'로 변경된 공지 포함
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 1906b6651137d95fe67b4ee68e146080d37f631f -->
