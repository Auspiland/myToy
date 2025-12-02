# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 지도 유틸리티.  
- **기술**: Python, GeoPandas/Shapely(STRtree 기반 공간 인덱스), GeoJSON, 기타 지오메트리 유틸리티.  
- **특징**: 사각형→행정구역 변환(대표 표현 포함), 섬 자동 감지 및 경계 조회, GeoJSON 생성·일괄 변환·고성능 배치 처리.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리, Kafka와 OpenSearch로 업로드하는 스트리밍 기반 E2E 파이프라인.  
- **기술**: Docker(멀티 컨테이너), Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy, Selenium(스크립트 수집 보조).  
- **특징**: 컨테이너 기반 네트워크 분리 및 compose 구성, Spark 스트리밍→Kafka→OpenSearch 연계, 한국어 전처리(오탈자·문장분리·불용어) 최적화.

## B_project
- **설명**: 알고리즘 문제 풀이/코딩테스트 연습용 라이브러리 및 자동화 도구 모음.  
- **기술**: Python(모듈화된 알고리즘 패키지), Jupyter 노트북, FastAPI/백엔드 운영 가이드 문서(참고용), LLM 연동 유틸리티.  
- **특징**: boj_bible(자료구조·그래프·문자열·고급 알고리즘) 모듈, CT 자동화 및 예제 노트북(문제 풀이 함수 포함), LLM 관련 유틸(기본 모델 변경 등) 및 운영·배포 가이드 문서.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: a98c7ddc46bbbb92420c071e00ed61e80b80634d -->
