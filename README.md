# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역이나 단일 좌표를 대한민국/북한 행정구역(시·도 등)으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, shapely/GeoPandas 기반 공간 색인(STRtree), GeoJSON, pip 패키지 의존성.  
- **특징**: 사각형→행정구역/좌표→행정구역 변환(대량 처리 지원), 행정구역 경계 조회 및 GeoJSON 생성·시각화, 섬 자동 감지 및 방향 기반 대표 표현 생성.

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트를 추출해 전처리하고 Kafka·Opensearch로 업로드하는 Docker화된 스트리밍 파이프라인입니다.  
- **기술**: Docker / docker-compose, Apache Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Nginx, Selenium, Kiwipiepy.  
- **특징**: 컨테이너 기반 분산 아키텍처(Shared-net), Spark로 파일 감시→Kafka 토픽·Opensearch 적재, Kiwipiepy+룰베이스 기반 문장 전처리(Streaming/Timeout 트리거 처리).

## B_project
- **설명**: 알고리즘 학습·코딩테스트 지원 라이브러리 및 자동화 도구 모음입니다.  
- **기술**: Python(라이브러리·노트북), 알고리즘 구현(그래프·트리·문자열·고급 알고리즘), 일부 LLM 연동 유틸리티.  
- **특징**: boj_bible(기초/그래프/트리/문자열/고급 알고리즘) 모듈, CT 자동화·기록 도구 및 LLM 호출 유틸(기본 모델 변경 안내 포함), 문제 풀이 노트북(.ipynb) 및 운영·배포 가이드 문서 포함.
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

<!-- LAST_PROCESSED_SHA: c75ebfce962a1a12a1014481bf11f74a99e990e7 -->
