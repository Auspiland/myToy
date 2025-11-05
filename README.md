# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 개별 좌표를 대한민국(남한/북한) 행정구역으로 빠르게 변환해주는 지리 공간 도구  
- **기술**: Python, Shapely/GeoPandas, STRtree 공간 인덱스, GeoJSON  
- **특징**: 사각형·좌표→행정구역 변환(광역/시도·시군구), 섬 지역 자동 감지 및 방향 기반 대표표현 생성, GeoJSON 생성·시각화 및 대량 JSON 일괄 처리

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·Opensearch 업로드까지의 컨테이너화된 스트리밍 E2E 파이프라인  
- **기술**: Docker 컴포즈, Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy  
- **특징**: 마운트된 폴더 감시→Spark로 Kafka 토픽 생산/소비 및 전처리, Kiwipiepy 기반 오탈자/문장 분리 처리(F.pandas_udf 활용), OpenSearch 연동 및 웹 검색 서비스 제공

## B_project
- **설명**: 알고리즘 학습·코딩테스트 풀이 지원과 자동화 도구를 모아둔 레포지토리  
- **기술**: Python 중심(알고리즘 라이브러리·유틸 스크립트), LLM 연동 유틸 포함  
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 라이브러리, CT 자동화·기록 도구, LLM 관련 유틸 기본 모델이 gpt-5→gpt-5-nano로 변경(스트리밍/폴백 지원)
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: bd1c84936b9268d5f301b765d7084fa981c92500 -->
