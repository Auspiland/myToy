# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국 행정구역(시/도/군/구 등)으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely/Geopandas 기반 공간 인덱스(STRtree), GeoJSON 처리.
- **특징**: 사각형→행정구역 변환(대량 처리 최적화), 좌표→행정구역 변환 및 경계 조회, 섬 자동 감지·GeoJSON 생성 및 파일 일괄 변환.

## Mini-Pipeline
- **설명**: YouTube 스크립트 추출부터 전처리·Kafka·OpenSearch 업로드까지 스트리밍 기반 E2E 파이프라인입니다.
- **기술**: Docker 컴포즈, Apache Spark(Structured Streaming), Kafka(kRaft), OpenSearch, FastAPI/Nginx.
- **특징**: Streaming 기반 파일 감시→Spark 처리→Kafka 토픽 연계, Kiwipiepy 기반 문장 전처리(udf 적용), OpenSearch 인덱싱 및 웹 검색 인터페이스.

## B_project
- **설명**: 알고리즘 학습 및 코딩 테스트 문제 해결을 위한 라이브러리/도구 모음입니다.
- **기술**: Python 중심(알고리즘/자료구조 구현).
- **특징**: boj_bible(기초 자료구조·그래프·트리·문자열·고급 알고리즘 모듈), 코딩 테스트 자동화 및 기록용 CT 도구.
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: b42a24e0cc53a62c5c4253b22d1fee8b27f21d1e -->
