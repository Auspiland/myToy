# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표나 사각형 영역을 대한민국(남한/북한) 행정구역으로 변환해 대표 텍스트·상세 정보를 제공하고 GeoJSON을 생성/시각화하는 도구입니다.
- **기술**: Python, Shapely/GeoPandas, STRtree 공간 인덱스, GeoJSON
- **특징**: 사각형→행정구역 변환 및 배치 처리, 섬 자동 감지(방향/면적 기반 대표표현), 행정구역 경계 조회·GeoJSON 생성

## Mini-Pipeline
- **설명**: YouTube URL → 문장 전처리 → Kafka/Opensearch 업로드까지 Docker 기반 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker, Kafka(kRaft), Apache Spark Structured Streaming, OpenSearch, FastAPI/Nginx, Kiwipiepy
- **특징**: Spark readStream으로 파일 감시·Kafka 토픽 처리·Opensearch 적재, 전처리는 Kiwipiepy + 룰베이스(UDF), 웹 검색 인터페이스 연동

## B_project
- **설명**: 알고리즘 문제 풀이 및 코딩 테스트 자동화·기록용 토이 프로젝트입니다.
- **기술**: Python 기반 알고리즘 라이브러리 및 스크립트
- **특징**: boj_bible(기초 자료구조·그래프·트리·문자열·고급 알고리즘 모듈), CT(코딩 테스트 자동화 및 기록 도구)
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 7e6b25b799fb39baf4888d393a3165388e2cf3e7 -->
