# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국/북한 행정구역(시/도 등)으로 변환하고 GeoJSON으로 생성·시각화하는 도구입니다.  
- **기술**: Python, Shapely/STRtree 기반 공간 인덱싱, GeoJSON, 행정경계 데이터(HDX/V-world).  
- **특징**: 사각형→행정구역 변환(대량 처리 지원), 섬 자동 감지 및 방향 기반 대표 표현 생성, 행정구역 경계 조회 및 GeoJSON 출력.

## Mini-Pipeline
- **설명**: YouTube URL로부터 스크립트를 추출해 문장 전처리 후 Kafka/Opensearch로 업로드하는 컨테이너화된 스트리밍 파이프라인입니다.  
- **기술**: Docker Compose(멀티컨테이너), Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리).  
- **특징**: Spark 기반 실시간 스트리밍 파이프라인(Kafka 토픽 입출력), Docker 네트워크로 서비스 분리·연결, 한국어 토크나이징·오탈자 수정 등 룰베이스 전처리.

## B_project
- **설명**: 알고리즘 문제 풀이용 라이브러리와 코딩 테스트 자동화·기록 도구 모음입니다.  
- **기술**: Python 기반 알고리즘 구현(자료구조, 그래프, 트리, 문자열 등), Jupyter 노트북, LLM 연동 유틸리티.  
- **특징**: boj_bible 알고리즘 모듈 모음, CT 자동화 도구(LLM 응답 유틸 포함) 및 기본 모델 변경 안내, kakao_history 노트북·운영·배포 관련 문서 수록.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 65bb87bebc090981e45f6a945abf39d46584df23 -->
