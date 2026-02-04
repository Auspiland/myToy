# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 단일 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python 기반(Shapely/GeoPandas/STRtree 등 공간 인덱스), GeoJSON, GitHub 자동 푸시 유틸.  
- **특징**: 사각형→행정구역 변환 및 다수 처리(convert_many), 섬 자동 감지 및 방향 기반 대표 표현 생성, 행정구역 경계 조회 및 GeoJSON 생성/시각화.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집해 문장 전처리 후 Kafka·Opensearch로 업로드하는 컨테이너 기반 스트리밍 파이프라인입니다.  
- **기술**: Docker Compose(컨테이너별 네트워크), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리).  
- **특징**: Spark readStream→Kafka→Opensearch의 E2E 스트리밍 ETL, 컨테이너 간 내부 네트워크·라우팅 구성(Nginx), Kiwipiepy 기반 오탈자 수정·문장 분리·불용어 처리(병렬 pandas_udf 사용).

## B_project
- **설명**: 알고리즘 연습과 코딩테스트 솔루션을 모아둔 프로젝트입니다.  
- **기술**: Python(알고리즘/자료구조 모듈), Jupyter 노트북 예제, FastAPI·DB 등 운영 가이드 문서(참고용).  
- **특징**: boj_bible(기본 자료구조·그래프·문자열·고급 알고리즘) 모듈화, CT 자동화·기록 도구 및 예제 노트북(kakao_history), CT 유틸의 LLM 기본 모델 파라미터(gpt-5 → gpt-5-nano) 변경 공지.
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
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 924e183207c25c755dfd30236b5e0d72b03a777e -->
