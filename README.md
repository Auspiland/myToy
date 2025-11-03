# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 매핑하고 GeoJSON으로 생성·시각화하는 도구입니다.
- **기술**: Python (Shapely/STRtree, GeoJSON), GeoPandas/지도 데이터, GitHub 연동 스크립트.
- **특징**: Rect2Region 기반 대량 변환 및 대표 텍스트 옵션, 섬 자동 감지 및 행정구역 경계 조회, GeoJSON 생성·시각화 및 성능 최적화(v2).

## Mini-Pipeline
- **설명**: Youtube 스크립트 수집 → 문장 전처리 → Kafka/Opensearch로 업로드하는 도커 기반 스트리밍 E2E 파이프라인입니다.
- **기술**: Docker-compose, Spark Structured Streaming, Kafka(kRaft), Opensearch, FastAPI/Nginx, Selenium, Kiwipiepy.
- **특징**: 마운트 폴더 감시를 통한 Spark→Kafka 파이프라인, Kiwipiepy 기반 전처리(pandas_udf 사용), 컨테이너 네트워크 설계 및 Opensearch 연동.

## B_project
- **설명**: 알고리즘 문제 풀이(백준)용 라이브러리와 코딩 테스트 자동화/기록 도구 모음입니다.
- **기술**: Python 기반 알고리즘 모듈(자료구조·그래프·트리·문자열 등), 자동화 스크립트, LLM 헬퍼 유틸리티.
- **특징**: boj_bible(기본/고급 알고리즘 모듈) 제공, CT 자동화 도구 및 LLM 호출 유틸리티(기본 모델이 gpt-5-nano로 변경됨), 스트리밍/폴백 지원.
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 453b75dadaa87d2fc441bad67d30ad7ddcc9d6c5 -->
