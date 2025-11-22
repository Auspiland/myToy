# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 입력 좌표나 사각형 영역을 대한민국(남한/북한) 행정구역으로 매핑하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely(STRtree) 기반 공간 인덱스, GeoJSON 처리 및 데이터 파일(국내·북한 경계).  
- **특징**: 빠른 사각형→행정구역 변환(대량 처리 지원), 섬 지역 자동 감지 및 대표 표현 생성, 경계 조회·GeoJSON 생성 및 시각화 기능.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집해 전처리·가공하여 Kafka와 Opensearch로 스트리밍 업로드하는 E2E 파이프라인입니다.  
- **기술**: Docker(멀티 컨테이너), Apache Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리).  
- **특징**: 컨테이너 기반 스트리밍 아키텍처 및 네트워크 분리, Kiwi + 룰베이스 전처리(pandas_udf)로 문장 분리·오탈자 수정, Spark↔Kafka↔Opensearch 연동을 통한 실시간 처리·검색 제공.

## B_project
- **설명**: 알고리즘 문제 풀이용 라이브러리와 코딩 테스트 자동화·기록 도구 모음입니다.  
- **기술**: Python 중심(라이브러리·노트북), Jupyter 노트북, FastAPI/비동기 구성 등 운영·배포 가이드 문서 포함.  
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT 자동화 도구 및 LLM 헬퍼 함수(기본 모델이 gpt-5-nano로 변경) 포함, 예제 노트북(kakao_history.ipynb) 및 운영·배포 가이드 문서 제공.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 456da6b1d7dccc82bc1ef009517a4ac73f670103 -->
