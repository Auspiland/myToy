# myToy - Toy Projects Monorepo
잡동사니 프로젝트들의 모음입니다.

<!-- AUTO-UPDATE:START -->
## geo_map
- **설명**: 사각형 영역 또는 좌표를 대한민국(남한/북한) 행정구역으로 변환하고 GeoJSON으로 시각화하는 도구입니다.
- **기술**: Python, Shapely(STRtree) 기반 공간 인덱싱, GeoJSON, 공간 데이터(행정구역) 파일.
- **특징**: 사각형/좌표→행정구역 변환(대표 텍스트 옵션), 섬 자동 감지 및 방향 기반 대표 표현, 경계 조회·GeoJSON 생성·JSON 배치 변환 지원.

## Mini-Pipeline
- **설명**: YouTube URL에서 스크립트 추출 후 문장 전처리하여 Kafka와 Opensearch로 업로드하는 Docker 기반 스트리밍 파이프라인입니다.
- **기술**: Docker Compose, Spark(Structured Streaming), Kafka(kRaft), Opensearch, FastAPI + Nginx, Kiwipiepy(한국어 전처리), Selenium(스크립트 수집 보조).
- **특징**: 폴더 감시 → Spark로 Kafka 토픽 생성 → 가공 후 Opensearch에 적재하는 E2E 스트리밍, Kiwipiepy 기반 오탈자·문장 분리 처리(pandas_udf 사용), 다중 컨테이너 네트워크(Shared-net/분리 네트워크)로 구성된 운영 환경.

## B_project
- **설명**: 알고리즘 연습 및 코딩 테스트용 유틸·라이브러리와 관련 도구들을 모아놓은 프로젝트입니다.
- **기술**: Python 중심(모듈·노트북), Jupyter 노트북, 테스트/스크립트용 유틸리티, LLM 연동 유틸(common_utils).
- **특징**: boj_bible(자료구조·그래프·트리·문자열·고급 알고리즘) 모듈화, CT(코딩테스트) 자동화 도구 및 예제 노트북 제공, LLM 호출 유틸의 기본 모델 변경 등 운영·개발 관련 문서·샘플 포함.
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 29fbed3d030388deac4235256fccd45ab61a3617 -->
