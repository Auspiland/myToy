# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 한반도 행정구역(시/도/시군구 등)으로 빠르게 매핑하고 GeoJSON을 생성·시각화하는 지오프로세싱 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간 인덱스, GeoJSON, 경계 데이터(대한민국/북한).  
- **특징**: 사각형→행정구역 고속 변환(rect2region_fast_v2), 섬 자동 감지 및 방향 기반 대표 표현, 일괄 JSON/GeoJSON 생성·시각화.

## Mini-Pipeline
- **설명**: YouTube 스크립트 수집부터 전처리(Kiwi), Kafka/Spark 스트리밍을 거쳐 Opensearch에 인덱싱하는 Docker 기반 E2E 파이프라인입니다.  
- **기술**: Docker Compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Selenium/Kiwipiepy.  
- **특징**: 컨테이너화된 스트리밍 아키텍처(다중 네트워크), Spark로 readStream/writeStream 파이프라인 구성, 텍스트 전처리용 pandas_udf + Kiwi 연동.

## B_project
- **설명**: 알고리즘 문제 풀이용 라이브러리(boj_bible)와 코딩 테스트 자동화·기록 도구를 포함한 실습용/운영용 프로젝트 모음입니다.  
- **기술**: Python 중심 코드베이스, FastAPI/Async DB·Redis(문서 참조), Docker Compose, LLM 유틸리티 통합.  
- **특징**: 기초·그래프·문자열 등 알고리즘 모듈(boj_bible), CT 자동화 도구와 LLM 호출 유틸(response_GPT 계열), kakao_history 노트북·운영 가이드(special_prompt.md) 추가.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: af2d163445af75978d377baf41b849baa4628275 -->
