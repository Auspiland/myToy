# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 경계/GeoJSON을 생성·시각화하는 도구입니다.  
- **기술**: Python, Shapely/GeoPandas, STRtree 공간 인덱스, GeoJSON.  
- **특징**: 고속 사각형→행정구역 변환(rect2region_fast_v2), 좌표→행정구역 및 경계 조회, GeoJSON 생성·섬 자동 감지.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리, Kafka와 Opensearch 업로드까지의 컨테이너화된 스트리밍 E2E 파이프라인입니다.  
- **기술**: Docker(여러 compose 네트워크), Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI, Kiwipiepy.  
- **특징**: Streaming 기반 파일→Kafka→Opensearch 흐름, Spark에서의 실시간 전처리(문장 분리·오탈자 수정), 검색용 Opensearch 인덱싱 및 웹 연동.

## B_project
- **설명**: 알고리즘 문제 풀이와 코딩 테스트 준비를 위한 파이썬 라이브러리 및 도구 모음입니다.  
- **기술**: Python 중심의 알고리즘/자료구조 구현.  
- **특징**: boj_bible(기본 자료구조·그래프·트리·문자열·고급 알고리즘), 코딩 테스트 자동화 및 기록 도구(CT).
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: fce1a70e77e4321b3161c51a2b84fe5f4473e5f7 -->
