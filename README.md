# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON 데이터.  
- **특징**: 사각형/좌표→행정구역 변환(대표문구 제공), 섬 자동 감지 및 방향 기반 대표표현, 행정경계 조회·GeoJSON 생성·JSON 일괄 변환.

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트를 추출해 문장 전처리 후 Kafka·Opensearch로 업로드하는 컨테이너화된 스트리밍 파이프라인입니다.  
- **기술**: Docker Compose, Apache Spark Streaming, Kafka(kRaft), OpenSearch, FastAPI, Nginx, Kiwipiepy, Selenium.  
- **특징**: 스트리밍 기반 ingest→가공→저장(파일→Spark→Kafka→OpenSearch), 서비스별 컨테이너·네트워크 분리 및 Nginx 라우팅, Kiwipiepy 기반 한국어 전처리와 룰베이스 정제.

## B_project
- **설명**: 알고리즘 학습·코딩테스트 풀이를 위한 라이브러리와 도구 모음입니다.  
- **기술**: Python 중심(모듈화된 알고리즘 패키지), Jupyter 노트북, FastAPI/비동기·운영 가이드 문서(운영/배포 참고).  
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈, CT(자동화/기록) 도구 및 kakao_history.ipynb 예제, AI/배포 관련 special_prompt 문서(설치·운영 가이드) 및 LLM 유틸 변경 사항 안내.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 40d7826e3ddbd7066d7f81d504dfec0eb36cb12d -->
