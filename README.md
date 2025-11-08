# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 좌표 또는 사각형 영역을 대한민국(남한/북한) 행정구역으로 빠르게 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, shapely(STRtree) 기반 공간색인, GeoJSON, geopandas 유사 처리
- **특징**: 사각형→행정구역 변환(최적화된 rect2region_fast_v2), 좌표→행정구역 매핑 및 섬 자동 감지, GeoJSON 생성·경계 조회·일괄 JSON 변환

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·인덱싱까지 Kafka·Spark·Opensearch를 이용한 엔드투엔드 스트리밍 파이프라인입니다.
- **기술**: Docker(컨테이너화), Apache Spark 스트리밍, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy
- **특징**: Spark readStream 기반 파일→Kafka→Opensearch 흐름, Kiwipiepy+룰 기반 한국어 전처리(Pandas UDF 활용), docker-compose로 분리된 네트워크 구성 및 컨테이너화

## B_project
- **설명**: 알고리즘 문제 풀이(백준) 및 코딩 테스트 자동화 도구 모음입니다.
- **기술**: Python 기반 알고리즘 라이브러리 및 유틸 스크립트, LLM 호출 유틸 포함
- **특징**: boj_bible(기본 자료구조·그래프·트리·문자열·고급 알고리즘 제공), CT(코딩 테스트 자동화/기록 도구), LLM 유틸 기본 모델이 gpt-5→gpt-5-nano로 변경된 공지 포함
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 9258816a3fc9a366f69078451a64e729c905ec57 -->
