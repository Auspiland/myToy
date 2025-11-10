# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역 단위로 빠르게 변환하고 시각화하는 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON, GeoPandas(데이터 기반).  
- **특징**: 사각형→행정구역 변환(대량 처리·최적화된 rect2region_fast_v2), 좌표→지역·경계 조회 및 섬 자동 감지, GeoJSON 생성 및 시각화/일괄 변환 기능.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·Kafka·OpenSearch 업로드까지의 컨테이너화된 E2E 스트리밍 파이프라인입니다.  
- **기술**: Docker(다중 compose 네트워크), Apache Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx.  
- **특징**: Streaming 기반 파일 감시→Kafka 토픽 전송→Spark 처리→OpenSearch 색인, Kiwipiepy 및 룰 기반 전처리(오탈자 수정·문장 분리 등), 컨테이너 네트워크/데브옵스 구성.

## B_project
- **설명**: 알고리즘 문제 풀이·코딩 테스트 연습용 라이브러리 및 자동화 도구 모음입니다.  
- **기술**: Python 중심 모듈화(알고리즘 구현 및 유틸), LLM 연동 유틸(자동화 도구에 사용).  
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘 모듈), CT(코딩 테스트 자동화/기록 도구), auto_solve의 LLM 기본모델을 gpt-5→gpt-5-nano로 변경한 설정 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 4c30ecb27bb4da978bb709f00514873cca42e0e3 -->
