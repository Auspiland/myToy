# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간 색인, GeoPandas/GeoJSON, 공간 경계 데이터.  
- **특징**: 사각형→행정구역 변환(배치 처리 가능), 섬 지역 자동 감지·방향 기반 대표 표현 생성, 행정구역 경계 조회 및 GeoJSON 생성/시각화.

## Mini-Pipeline
- **설명**: YouTube URL에서 스크립트 추출해 문장 전처리 후 Kafka·OpenSearch로 업로드하는 컨테이너형 스트리밍 파이프라인입니다.  
- **기술**: Docker(Compose), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Selenium, Kiwipiepy.  
- **특징**: 컨테이너화된 E2E 스트리밍 아키텍처, Spark로 마운트 폴더 감시→Kafka 토픽 처리→OpenSearch 적재, 한국어 전처리(키위·룰베이스) 병렬 처리 최적화.

## B_project
- **설명**: 알고리즘/코딩 테스트 풀이용 라이브러리 및 코딩 테스트 자동화 도구 모음입니다.  
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열 등), Jupyter 노트북, FastAPI/Async 관련 운영 가이드 문서.  
- **특징**: boj_bible(기본·그래프·트리·문자열·고급 알고리즘) 모듈, CT 자동화·기록 도구 및 LLM 유틸(response_GPT 등, 기본 모델 변경 안내), 참고용 노트북·운영·배포 가이드 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 0a7963df8ece61af22ab146dd7119529026410af -->
