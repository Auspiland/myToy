# geo_map

좌표 또는 사각형 영역을 한반도(남한/북한) 행정구역으로 변환하는 프로젝트

<!-- AUTO-UPDATE:START -->
## 주요 기능

- 사각형 영역 → 행정구역 변환 (광역시/도 단위)
- 좌표 → 행정구역 변환
- 섬 지역 자동 감지 (예: "제주특별자치도 남서부 섬")
- 행정구역 경계 정보 조회
- GeoJSON 파일 생성 및 시각화
- JSON 파일 일괄 변환

## 빠른 시작

### 설치

```bash
pip install -r requirements.txt
```

### 기본 사용법

```python
from config import BASE_PATH
from core.rect2region_fast_v2 import Rect2Region
import os

# Rect2Region 인스턴스 생성 (최적화된 최신 버전)
converter = Rect2Region()

# 사각형 좌표 정의 (4개의 [경도, 위도] 좌표)
rect_coords = [
    [126.93167575079963, 37.10178611970895],
    [127.50557082786963, 37.10314793150034],
    [126.93507098285538, 36.64210788827871],
    [127.50553754496315, 36.643447265652945]
]

# 변환 실행 (대표 텍스트만 필요한 경우)
result = converter.convert(rect_coords, only_representive_text=True)
print(result['representative'])
# 출력: ['대한민국 충청남도 천안시 서북구 성거읍 중심', '충청남도 북동부 포함', ...]

# 상세 정보 필요한 경우
result = converter.convert(rect_coords)
converter.show(result)

# GeoJSON 파일 생성
output_path = os.path.join(BASE_PATH, "static", "result.geojson")
converter.create_geojson(rect_coords, output_path, result=result, openbrowser=True)
```

## 핵심 모듈: Rect2Region

### 주요 메서드

#### `convert(rect_coords, only_representive_text=False)`

사각형 영역에 포함되는 행정구역을 분석합니다.

**입력:**
- `rect_coords`: 4개의 좌표 리스트 `[[lon, lat], ...]`
- `only_representive_text`: True일 경우 대표 텍스트만 반환 (성능 최적화)

**반환값:**
```python
{
    "representative": ["경기도 남부 포함", "충청북도 북부 포함"],  # 광역 단위 대표 표현
    "fully_contained": ["천안시", "아산시"],                    # 완전히 포함된 지역
    "all_regions": ["천안시", "아산시", "평택시"],              # 전체 지역 (완전+일부)
    "provincial_regions": ["경기도", "충청북도"],               # 시/도 단위 지역
    "center": [127.2, 36.9],                                   # 사각형 중심 좌표
    "distance_info": None
}
```

**대표 표현 규칙:**
- 면적 95% 이상 포함: "서울특별시 전체"
- 면적 70% 이상 포함: "서울특별시 대부분"
- 섬 지역 40% 이상: "제주특별자치도 남서부 섬"
- 그 외: "강원도 북부 포함" (방향 기반)

#### `convert_many(rect_coords_list, only_representive_text=False)`

여러 개의 사각형을 한 번에 변환합니다 (진행률 표시).

```python
rect_coords_list = [rect1, rect2, rect3, ...]  # 2,000개
results = converter.convert_many(rect_coords_list, only_representive_text=True)
```

**성능:** 2,000개 처리 시 약 1.6분 소요 (평균 0.048초/건)

#### `get_region_boundary(region_name)`

특정 행정구역의 경계 정보를 반환합니다.

```python
result = converter.get_region_boundary("서울특별시")
# {
#     "found": True,
#     "name": "서울특별시",
#     "bounds": [min_lon, min_lat, max_lon, max_lat],
#     "center": [lon, lat],
#     "boundary_coords": [[lon, lat], ...]
# }
```

#### `create_geojson(rect_coords, output_path, result=None, openbrowser=False)`

사각형과 포함된 행정구역을 GeoJSON 파일로 생성하고 GitHub에 푸시합니다.

**생성되는 GeoJSON 구조:**
- 입력 사각형 폴리곤
- 포함된 시/도 경계 폴리곤
- 각 시/도의 중심점

#### `convert_json_file(input_file, output_file)`

JSON 파일의 좌표 데이터를 일괄 변환합니다.

```python
using_data_path = os.path.join(BASE_PATH, "using_data")
input_file = os.path.join(using_data_path, "data.json")
output_file = os.path.join(using_data_path, "converted_data.json")
converter.convert_json_file(input_file, output_file)
```

## 프로젝트 구조

```
geo_map/
├── config.py                    # 환경 설정 (BASE_PATH 정의)
├── main.py                      # 메인 실행 예제
├── requirements.txt             # 의존성 패키지
│
├── core/                        # 핵심 기능 모듈
│   ├── rect2region_fast_v2.py   # 사각형 → 행정구역 변환 (최신 배포판) ⭐
│   ├── rect2region_fast.py      # 성능 최적화 버전 (v1)
│   ├── rect2region.py           # 원본 버전
│   ├── point2region.py          # 좌표 → 행정구역 변환
│   └── rect2geojson.py          # 사각형 → GeoJSON 변환
│
├── scripts/                     # 유틸리티 스크립트 (독립 실행)
│   ├── README.md                # 스크립트 상세 문서
│   ├── coord2region.py          # OSM 기반 지역 매칭
│   ├── translate_regionname.py  # 북한 지명 번역 (LLM)
│   ├── check_shapefile.py       # Shapefile 검증/변환
│   └── ...                      # 경계 데이터 처리 파이프라인
│
├── src/
│   ├── __init__.py              # 패키지 초기화 (추가)
│   └── common_utils.py          # LLM API 호출, GitHub 푸시 등
│
├── using_data/                  # 핵심 행정구역 GeoJSON 데이터 ⭐
│   ├── boundaries_KR_20220407_modified.geojson  # 대한민국 (최종본)
│   ├── new_prk_admbnda_adm2_wfp_20190624.geojson  # 북한 (최종본)
│   └── ...                      # 기타 참조 데이터
│
├── static/                      # 생성된 GeoJSON 파일 저장
│   └── whole.geojson            # 전체 시/도 경계 + 중심점
│
└── history/                     # 개발 과정 문서
    ├── README_v1.md             # 이전 README
    ├── RECT2REGION_FAST_V2_README.md  # v2 업그레이드 가이드
    ├── OPTIMIZING_REPORT.md     # 성능 최적화 보고서
    └── ...                      # 경계 처리 보고서
```

## 핵심 데이터 파일

### 1. 대한민국 행정구역 (최종본)
- **파일:** `using_data/boundaries_KR_20220407_modified.geojson`
- **출처:**
  - [Humanitarian Data Exchange - South Korea Kontur Boundaries](https://data.humdata.org/dataset/kontur-boundaries-korea-republic-of)
  - V-world 공공 데이터 (시/도 레벨)
- **내용:** 리 수준까지의 대한민국 폴리곤 데이터
- **특징:**
  - 경기도/강원도 북부 국경선 수정 (개미굴 메우기 적용)
  - Right-hand rule 적용 완료

### 2. 북한 행정구역 (최종본)
- **파일:** `using_data/new_prk_admbnda_adm2_wfp_20190624.geojson`
- **출처:** [Humanitarian Data Exchange - North Korea Administrative Boundaries](https://data.humdata.org/dataset/cod-ab-prk)
- **내용:** 구, 군, 구역 수준의 북한 폴리곤 데이터
- **특징:** LLM을 활용한 한국어 지명 번역 완료 (ADM0_KO, ADM1_KO, ADM2_KO)

### 행정구역 레벨
국 > 도/특별시/광역시 > 시/군/구/구역 > 읍/면/동 > 리/통/지구 > 반

## 버전 및 최적화

### 현재 배포판: rect2region_fast_v2.py

**주요 기능:**
- Spatial Index (STRtree) 기반 O(log n) 검색
- Provincial Features 사전 필터링 (3,000개 → 17개)
- 섬 지역 자동 감지 (40% 임계값)
- 교차 영역 중심 기반 방향 계산
- Region Centers 캐싱

**성능:**
- 10개 변환: 0.475초 (평균 0.048초/건)
- 2,000개 변환: 약 96초 (1.6분)
- 기존 버전 대비 **10~30배 속도 향상**

### 버전 비교

| 항목 | rect2region.py | rect2region_fast.py | rect2region_fast_v2.py |
|------|----------------|---------------------|------------------------|
| 섬 감지 기능 | ✅ | ❌ | ✅ |
| 개선된 방향 계산 | ✅ | ❌ | ✅ |
| Spatial Index | ❌ | ✅ | ✅ |
| Provincial 필터링 | ❌ | ✅ | ✅ |
| 성능 (2,000개) | ~30분 | ~1.6분 | ~1.6분 |
| 기능 완전성 | 100% | 80% | 100% |

**자세한 내용:** `history/RECT2REGION_FAST_V2_README.md`, `history/OPTIMIZING_REPORT.md` 참조

## Scripts 디렉토리

독립적인 유틸리티 및 데이터 처리 스크립트 모음입니다.

### 주요 유틸리티
- `coord2region.py`: Shapefile 기반 좌표 → 지역명 변환
- `translate_regionname.py`: LLM 기반 북한 지명 한글 번역
- `check_shapefile.py`: Shapefile 검증 및 GeoJSON 변환

### 경계 데이터 처리 파이프라인
```
1. fix_border_ant_tunnels.py      # 국경선 개미굴 메우기
2. fix_border_properly.py         # 경기도/강원도 경계 교체
3. process_boundaries_v2.py       # 경계선 구간 추출
4. replace_boundaries_v4.py       # 경계선 교체
5. apply_right_hand_rule.py       # Right-hand rule 적용
6. show_all_geojson.py            # 최종 whole.geojson 생성
```

**자세한 내용:** `scripts/README.md` 참조

## 의존성

```txt
shapely
geopandas
pandas
```

## 사용 예시

자세한 사용 예시는 `main.py` 파일을 참조하세요.

```python
# main.py 예시
from core.rect2region_fast_v2 import Rect2Region

converter = Rect2Region()

# 1. 충청 지역 변환
rect_coords = [[126.93, 37.10], [127.50, 37.10], [126.93, 36.64], [127.50, 36.64]]
result = converter.convert(rect_coords)
converter.show(result)

# 2. 서울 전체
rect_coords_seoul = [[126.7, 37.7], [127.3, 37.7], [126.7, 37.4], [127.3, 37.4]]
result2 = converter.convert(rect_coords_seoul)
# 출력: ['서울특별시 전체', ...]

# 3. 바다 (범위 밖 - 가장 가까운 행정구역)
rect_coords_ocean = [[120.0, 35.0], [121.0, 35.0], [120.0, 34.0], [121.0, 34.0]]
result3 = converter.convert(rect_coords_ocean)
# distance_info에 가장 가까운 행정구역 정보 포함

# 4. JSON 파일 일괄 변환
converter.convert_json_file("using_data/data.json", "using_data/converted_data.json")
```

## 버전 히스토리

### v2.0 (2025-10-27)
- rect2region_fast_v2.py 배포
- rect2region.py의 섬 감지 기능을 최적화 버전에 통합
- Spatial index 구조 개선 (안정성)
- 모든 기능 + 최적화 통합 완료

### rect2region.py 섬 감지 기능 추가 (2025-10-27)
- 멀티폴리곤에서 섬과 내륙 자동 구분
- 교차 영역 중 섬이 40% 이상 차지 시 "섬" 표기 (예: "제주특별자치도 남부 섬")
- 방향 계산 로직 개선: 행정구역 중심 → 겹친 영역의 중심 방향
- intersection 재사용으로 성능 최적화
- 자세한 내용: `history/UPDATE_NOTE.md` 참조

### v1.0 (2025-10-24)
- rect2region_fast.py 개발
- Spatial Index (STRtree) 도입
- Provincial features 사전 필터링
- 10~30배 성능 향상

### Scripts v2 (2025-10-28)
- common_constants.py 모듈화
- 로깅 시스템 도입
- 하드코딩 경로 제거
- 에러 핸들링 개선
- 자세한 내용: `scripts/README.md` 참조

### 경계 데이터 처리 완료 (2025-10-27)
- 경기도/강원도 북부 국경선 수정 완료
- boundaries_KR_20220407_modified.geojson 최종본 생성
- Right-hand rule 적용
- 자세한 내용: `history/README_border_fix_v2.md` 참조

## 참고 문서

- `history/README_v1.md` - 이전 README (기능 상세 설명)
- `history/RECT2REGION_FAST_V2_README.md` - v2 업그레이드 가이드
- `history/OPTIMIZING_REPORT.md` - 성능 최적화 상세 보고서
- `history/UPDATE_NOTE.md` - 섬 감지 기능 추가 노트
- `history/README_border_fix_v2.md` - 경계 데이터 처리 과정
- `scripts/README.md` - 스크립트 상세 문서

## 라이선스

MIT License

---
<!-- AUTO-UPDATE:END -->

<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: f7c0b7fbcaf8a5a32e72ce0d92a4f576a09920b0 -->
