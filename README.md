# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남·북한 포함) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/STRtree 기반 공간 인덱스, GeoJSON, geopandas 스타일 데이터 처리
- **특징**: 사각형→행정구역 변환(빠른 v2), 좌표→행정구역 변환 및 섬 자동 감지, GeoJSON 생성·일괄 JSON 변환

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 문장 전처리·Kafka·Opensearch 업로드까지의 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker(컨테이너화), Spark 스트리밍, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy
- **특징**: Spark 기반 스트리밍 파이프라인→Kafka 토픽/Opensearch 저장, Kiwipiepy+룰베이스 전처리(Pandas UDF), 컨테이너 네트워크로 서비스 연동

## B_project
- **설명**: 알고리즘 문제 풀이 및 코딩 테스트 자동화/기록을 위한 레포지토리입니다.
- **기술**: Python 기반 알고리즘 라이브러리(자료구조·그래프·트리·문자열·고급 알고리즘), LLM 헬퍼 유틸
- **특징**: boj_bible(문제 풀이용 모듈 집합), CT 자동화 도구(솔루션 기록·자동 실행), LLM 유틸 기본 모델이 gpt-5→gpt-5-nano로 변경 안내
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 57f7e4d6b1eda12f45454b3a4209fd50396b0171 -->
