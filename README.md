# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간 인덱스, GeoJSON, pandas 등.  
- **특징**: 사각형→행정구역 변환 및 대량 처리(convert_many), 섬 지역 자동 감지·대표 표현 규칙, 행정구역 경계 조회 및 GeoJSON 생성/출력.

## Mini-Pipeline
- **설명**: YouTube 스크립트를 입력으로 받아 전처리 후 Kafka→Spark→Opensearch로 업로드하는 컨테이너화된 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker(다중 compose 네트워크), Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Kiwipiepy, Selenium(수집 보조).  
- **특징**: Spark로 폴더 감시→Kafka 토픽 생산/소비·전처리(키위 기반 UDF), Opensearch에 색인 및 웹 검색, 컨테이너별 네트워크 분리와 배포 구성.

## B_project
- **설명**: 알고리즘 문제 풀이와 코딩 테스트 자동화·기록을 위한 라이브러리 및 도구 모음입니다.  
- **기술**: Python 주요(라이브러리/노트북), Jupyter Notebook, FastAPI/LLM 유틸(프로젝트 내 도구).  
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 제공, CT 자동화·기록 도구 및 LLM 연동 유틸(기본 모델 변경 이력 포함), 예제/노트북(kakao_history) 추가.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 0704f482a4f1f42a978bae2939eb713432775113 -->
