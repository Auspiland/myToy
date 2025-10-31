# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표나 사각형 영역을 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.  
- **기술**: Python, Shapely(STRtree) 기반 공간 인덱스, GeoJSON, 공간 데이터 처리용 라이브러리.  
- **특징**: 사각형→행정구역/좌표→행정구역 변환, 섬 자동 감지 및 방향 기반 대표 표현, GeoJSON 생성·시각화 및 대량 JSON 일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리 후 Kafka·Opensearch로 업로드하는 E2E 스트리밍 파이프라인입니다.  
- **기술**: Docker(컴포즈), Spark 스트리밍, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Selenium/Kiwipiepy(전처리).  
- **특징**: Spark 기반 실시간 파일 감시→Kafka 토픽 처리→OpenSearch 색인, 컨테이너 기반 네트워크 구성 및 Streaming 모드 전체 파이프라인.

## B_project
- **설명**: 알고리즘 문제 풀이와 코딩테스트 준비를 위한 파이썬 라이브러리·도구 모음입니다.  
- **기술**: Python 중심(알고리즘/자료구조 구현).  
- **특징**: boj_bible(기본 자료구조·그래프·트리·문자열·고급 알고리즘 모듈), 코딩테스트 자동화 및 기록 도구(CT).
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 78cfb73926c460b7c4a57aaf72d5a33e3dab3b5d -->
