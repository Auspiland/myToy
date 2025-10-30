# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## [geo_map]
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역 명칭으로 빠르게 변환하고 GeoJSON으로 시각화하는 툴입니다.
- **기술**: Python, geopandas/shapely, STRtree 공간 인덱스, GeoJSON 처리, LLM(지명 번역 보조).
- **특징**: 고성능 사각형→행정구역 변환(rect2region_fast_v2), 행정구역 경계 조회·GeoJSON 생성 및 시각화, 섬 자동 감지·대표 표현 규칙 적용.

## [Mini-Pipeline]
- **설명**: YouTube 스크립트 추출부터 문장 전처리·카프카 전송·Opensearch 업로드까지의 E2E 스트리밍 파이프라인입니다.
- **기술**: Docker(컨테이너화), Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Kiwipiepy(한국어 전처리).
- **특징**: 마운트 폴더 기반 스트리밍 입력 → Spark로 Kafka/Opensearch 출력, Kiwipiepy 기반 오탈자·문장 분리 전처리(pandas_udf), 컨테이너 네트워크로 서비스 통합 및 검색 UI 연동.

## [B_project]
- **설명**: 알고리즘 연습과 코딩 테스트 자동화·기록을 위한 도구 모음입니다.
- **기술**: Python 기반 라이브러리 및 스크립트.
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘 모듈) 제공, 코딩 테스트 자동화·기록(CT) 도구 포함.
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: f1984fe042a455185db8a4b3c0e8996eb8193f60 -->
