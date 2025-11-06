# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구  
- **기술**: Python, Shapely/GEOS(STRtree), GeoJSON, Pandas 등 공간 데이터 처리 스택  
- **특징**: 광역·시군구 단위 변환(대량처리 지원), 섬 자동 감지 및 대표 텍스트 생성, 행정구역 경계 조회 및 GeoJSON 출력

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출 → 전처리 → Kafka/Spark → OpenSearch 업로드까지의 컨테이너화된 E2E 스트리밍 파이프라인  
- **기술**: Docker/Compose, Apache Kafka(kRaft), Apache Spark, OpenSearch, FastAPI, Nginx, Kiwipiepy  
- **특징**: 스트리밍 기반 자동화 파이프라인, 텍스트 전처리(Kiwi·룰베이스) 및 Spark 스트리밍-Opensearch 연동, 컨테이너 네트워크 분리 구성

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트 자동화 도구 모음(백준 풀이 라이브러리 포함)  
- **기술**: Python 중심(자료구조·그래프·트리·문자열 알고리즘 등), LLM 연동 유틸리티  
- **특징**: boj_bible 알고리즘 모듈 집합, 코딩 테스트 자동화·기록 도구, LLM 호출 유틸(기본 모델 변경 등 설정 관리)
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: ccaa8519a67467758210a1770a31dacdd52ee3c0 -->
