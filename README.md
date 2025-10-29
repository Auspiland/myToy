# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역 단위로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간색인, GeoJSON, Spatial 데이터 처리 라이브러리.  
- **특징**: 사각형/포인트 → 행정구역 변환(대표 문구 포함), 섬 지역 자동 감지 및 방향 기반 대표 표현 생성, 행정구역 경계 조회 및 GeoJSON 생성/출력.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리, Kafka/Opensearch 업로드까지의 컨테이너화된 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker(다중 compose), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Kiwipiepy.  
- **특징**: Spark readStream 기반 파일→Kafka→Opensearch 흐름, Kiwipiepy·룰베이스를 이용한 오탈자 수정·문장 분리·불용어 처리, 컨테이너 네트워크로 구성된 모듈화된 아키텍처와 웹 검색 인터페이스.

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트 풀이를 위한 파이썬 라이브러리·도구 모음입니다.  
- **기술**: Python 중심(문제 풀이용 라이브러리 및 스크립트).  
- **특징**: 기본 자료구조·그래프·트리·문자열·고급 알고리즘(네트워크 플로우) 모듈 구성, 코딩 테스트 자동화 및 기록용 도구 제공.
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: e046db7339dc85f0afc7c943a45ca17f1332b83e -->
