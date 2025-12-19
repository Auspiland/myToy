# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(및 북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 툴
- **기술**: Python, Shapely/STRtree 기반 공간 인덱스, GeoJSON 데이터
- **특징**: 사각형·포인트 → 행정구역 변환(대표문구/상세), 섬 자동 감지 및 방향·면적 기반 대표 표현, 경계 조회·GeoJSON 일괄 생성 및 대량 처리 기능

## Mini-Pipeline
- **설명**: YouTube 스크립트 수집 → 문장 전처리 → Kafka/Opensearch로 업로드하는 E2E 스트리밍 파이프라인
- **기술**: Docker(Compose), Apache Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Selenium(스크립트 수집), Kiwi(한국어 전처리)
- **특징**: 컨테이너화된 멀티서비스 아키텍처(네트워킹 구성 포함), Spark로 폴더 감시→Kafka 토픽 생산→Opensearch 적재 흐름, Kiwipiepy 기반 문장 분리·오탈자·불용어 처리(udf/pandas_udf)

## B_project
- **설명**: 알고리즘 학습·코딩테스트 지원과 관련 도구들을 모아둔 저장소
- **기술**: Python 기반 알고리즘 코드베이스, Jupyter 노트북, FastAPI 관련 운영 문서(가이드)
- **특징**: boj_bible(자료구조·그래프·문자열·고급 알고리즘) 모듈, CT 자동화·LLM 유틸(기본 모델 파라미터 변경 등) 및 문제 풀이 노트북(예제 함수) 포함
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

<!-- LAST_PROCESSED_SHA: 2e6811187319dcfed574d36e6358adc88ee489d8 -->
