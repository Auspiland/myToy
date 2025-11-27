# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 입력한 좌표나 사각형 영역을 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely(STRtree)/GeoPandas, GeoJSON, spatial 인덱싱, GitHub 연동 스크립트.  
- **특징**: 사각형→행정구역 변환(대표문구/상세), 점→지역 매핑, 섬 자동 감지·GeoJSON 생성 및 배포(배치 JSON 변환 포함).

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·Kafka·Spark·Opensearch 업로드까지의 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker Compose, Kafka(kRaft), Spark Structured Streaming, OpenSearch, FastAPI, Nginx, Selenium, Kiwipiepy.  
- **특징**: 컨테이너 기반 스트리밍 파이프라인(파일 감시→Kafka 토픽→가공→Opensearch 저장), Kiwi 기반 텍스트 전처리(pandas_udf 적용), 웹 검색 인터페이스 연동.

## B_project
- **설명**: 알고리즘 문제 풀이/코딩 테스트 연습용 라이브러리와 관련 도구 모음입니다.  
- **기술**: Python(모듈화된 알고리즘 패키지), Jupyter 노트북, FastAPI·Async 도구 문서(참고용).  
- **특징**: BOJ용 알고리즘 모듈(자료구조·그래프·트리·문자열·고급 알고리즘), CT 자동화 및 기록 도구, CT 유틸에 포함된 LLM 유틸 기본모델이 gpt-5→gpt-5-nano로 변경(명시적 모델 지정 가능).
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: b0ab0390e2265413c4967771ce82d454fa32dddf -->
