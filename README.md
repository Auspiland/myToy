# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 매핑하고 GeoJSON으로 시각화하는 도구  
- **기술**: Python, Shapely(STRtree), GeoJSON, 공간 인덱싱/처리(권역 필터링)  
- **특징**: 사각형→행정구역 변환(대량 처리 지원), 좌표→행정구역 변환 및 경계 조회, 섬 감지·GeoJSON 생성 및 일괄 변환

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 후 문장 전처리 → Kafka 및 OpenSearch로 업로드되는 E2E 스트리밍 파이프라인  
- **기술**: Docker(컨테이너화), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwi(한국어 전처리)  
- **특징**: 컨테이너화된 마이크로서비스 아키텍처, Spark로 파일 감시→Kafka 토픽 처리→OpenSearch 색인화, 스트리밍 전처리(오탈자·문장분리·불용어)

## B_project
- **설명**: 알고리즘/코딩테스트 풀이용 라이브러리 및 코딩 테스트 자동화 도구 모음  
- **기술**: Python 기반 알고리즘 모듈(그래프/트리/문자열/고급 알고리즘), Jupyter 노트북 및 FastAPI·Async 유틸 문서화  
- **특징**: boj_bible(자료구조·알고리즘 모듈), CT 자동화(LLM 연동 유틸 포함) 및 문제별 예제·노트북, 운영·개발 가이드 문서 제공
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 2a7a0ccd1bb0215d36f41e58085099c611140f3c -->
