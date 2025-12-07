# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 라이브러리입니다.
- **기술**: Python, geopandas/shapely, STRtree 공간인덱스, GeoJSON
- **특징**: 사각형→행정구역 변환(대·시도 단위 방향/대표 표현), 좌표→행정구역 변환 및 섬 자동 감지, GeoJSON 생성·일괄 변환 지원

## Mini-Pipeline
- **설명**: YouTube 스크립트를 수집·전처리하여 Kafka와 OpenSearch로 스트리밍 업로드하는 E2E 파이프라인입니다.
- **기술**: Docker(컨테이너화), Spark Structured Streaming, Kafka(kRaft), OpenSearch, FastAPI/Nginx, Kiwipiepy
- **특징**: 전체 스트리밍 아키텍처(컨테이너 네트워크 별도 구성), Spark→Kafka→OpenSearch 데이터 흐름, 전처리(토큰화·오탈자 보정 등)와 검색 인터페이스 연동

## B_project
- **설명**: 알고리즘 문제 풀이·코딩 테스트 도구 모음(boj_bible)과 CT 자동화·보조 도구 모듈입니다.
- **기술**: Python(알고리즘 구현), 관련 유틸(노트북·FastAPI·Docker 문서), LLM 유틸리티(gpt-5-nano 기본 설정)
- **특징**: 자료구조·그래프·문자열 등 알고리즘 라이브러리(boj_bible), 코딩 테스트 자동화·예제 노트북, LLM 기반 응답 유틸 기본 모델 변경 및 운영 가이드 자료
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 8755fd445eaeb7cc97b56405b68e957f1c739c67 -->
