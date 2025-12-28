# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표(단일 포인트) 또는 사각형 영역을 대한민국(남한/북한) 행정구역(시/도 등)으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간 인덱스, GeoJSON, 공간 경계 데이터(GeoJSON).  
- **특징**: 사각형→행정구역(대표 텍스트/상세) 변환, 섬 자동 감지 및 경계 조회, GeoJSON 생성·일괄 변환 및 시각화 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리, Kafka와 OpenSearch로의 실시간 업로드까지 수행하는 E2E 스트리밍 파이프라인입니다.  
- **기술**: Docker(다중 compose·네트워크), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Selenium/Kiwipiepy(한국어 전처리).  
- **특징**: 마운트 폴더 → Spark로 읽어 Kafka 토픽에 송신 → 추가 가공 후 OpenSearch 인덱싱, Kiwi 기반 UDF로 문장 분리·오탈자 수정·불용어 처리, 컨테이너화된 멀티서비스 아키텍처.

## B_project
- **설명**: 알고리즘·코딩 테스트 연습용 라이브러리 및 자동화 도구 모음입니다.  
- **기술**: Python(알고리즘 모듈, Jupyter 노트북), FastAPI/Async 관련 유틸 문서(운영 가이드 포함), LLM 호출 유틸(공통 유틸).  
- **특징**: boj_bible(자료구조·알고리즘 모듈) 제공, CT(코딩 테스트) 자동화 및 노트북 예제(kakao_history.ipynb), LLM 호출 기본 모델 변경(gpt-5 → gpt-5-nano) 안내 및 특화 운영 문서 포함.
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

<!-- LAST_PROCESSED_SHA: 9dcf706d53abe8bad4e557fffdee399382d0442e -->
