# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, shapely/STRtree, GeoJSON, geopandas(및 관련 공간처리 라이브러리).
- **특징**: 사각형/좌표 → 행정구역 변환, 섬 지역 자동 감지 및 방향 기반 대표 표현, GeoJSON 생성·시각화 및 대량 JSON 일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 전처리해 Kafka와 OpenSearch로 업로드하는 컨테이너화된 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker(Compose), Apache Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI + Nginx, Kiwipiepy.
- **특징**: Spark 기반 스트리밍 ingest → Kafka/Opensearch 저장, Kiwipiepy·룰베이스 전처리(오탈자·문장분리 등), 여러 컨테이너로 구성된 네트워크·배포 구성.

## B_project
- **설명**: 알고리즘 연습 및 코딩 테스트 자동화용 유틸리티와 문제 풀이 모음입니다.
- **기술**: Python(알고리즘 라이브러리, Jupyter 노트북), FastAPI/Async 관련 도구 문서(운영 가이드 참조).
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT 자동화 도구(LLM 연동 함수 포함) 및 문제 풀이 노트북·운영 가이드 문서 추가.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 76373781fd71e400bf5baed88741a237a1d439f7 -->
