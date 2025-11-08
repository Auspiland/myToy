# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 한반도(남북) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python 기반(Shapely/STRtree 공간 인덱스, GeoJSON 처리), GeoJSON 데이터, LLM 보조 번역/유틸.  
- **특징**: 사각형→행정구역 변환(대표문구/상세 결과), 좌표→행정구역 변환 및 경계 조회, 섬 자동 감지·GeoJSON 생성 및 배포 지원.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka/Opensearch 업로드까지의 E2E 스트리밍 파이프라인입니다.  
- **기술**: Docker 컴포즈 기반 컨테이너 오케스트레이션, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy.  
- **특징**: Spark로 파일/스트림 감시·처리→Kafka/Opensearch 저장, 한국어 전처리(Kiwi)와 판다스 UDF 최적화, 멀티컨테이너 네트워크 구성 및 디버깅 지원.

## B_project
- **설명**: 알고리즘 학습 및 코딩테스트 해결을 위한 라이브러리 및 자동화 도구 모음입니다.  
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열·고급 알고리즘), CT 자동화 스크립트, LLM 연동 유틸.  
- **특징**: boj_bible로 알고리즘 구현 모듈 제공, 코딩테스트 자동화(전처리·해결 워크플로우), LLM 관련 공통 유틸의 기본 모델(gpt-5→gpt-5-nano) 변경 안내.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: bab39bc911f8fd5cde1948688b50919e16806378 -->
