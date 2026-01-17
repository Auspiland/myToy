# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON 형태로 시각화하는 도구입니다.  
- **기술**: Python 기반(Shapely/GeoJSON 기반 공간처리, STRtree 등 공간 인덱스), GeoJSON 데이터 사용.  
- **특징**: 사각형→행정구역 변환(고속화된 rect2region_fast_v2), 섬 자동 감지 및 방향 기반 대표표현, GeoJSON 생성·일괄 변환 및 행정구역 경계 조회.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리, Kafka/Opensearch 적재까지의 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker(컨테이너 오케스트레이션), Apache Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy.  
- **특징**: Streaming 기반 파이프라인(파일 감시 → Kafka 토픽 → Spark 처리 → Opensearch 적재), Kiwi 기반 텍스트 전처리(pandas_udf 활용), Docker-compose 네트워크 분리로 서비스 분산 구성.

## B_project
- **설명**: 알고리즘·코딩 테스트 학습용 라이브러리 및 자동화 도구들을 모아 놓은 프로젝트입니다.  
- **기술**: Python 중심(알고리즘 구현, 노트북 코드 및 FastAPI/Async 관련 운영 문서 포함).  
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT(코딩테스트 자동화·기록) 도구와 예제 노트북, LLM 연동 유틸 및 운영·개발 가이드 문서 포함.
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

<!-- LAST_PROCESSED_SHA: 44141ec5e7f5f7d7cc6eb5507aef64465bc4fb83 -->
