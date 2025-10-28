# geo_map

좌표 또는 사각형 영역을 한반도(남한/북한) 행정구역으로 변환하는 프로젝트

## 시작하기

### 기본 사용법

```python
import config
from config import BASE_PATH
from core.rect2region import Rect2Region
import os

# Rect2Region 인스턴스 생성
converter = Rect2Region()

# 사각형 좌표 정의 (4개의 [경도, 위도] 좌표)
rect_coords = [
    [126.93167575079963, 37.10178611970895],
    [127.50557082786963, 37.10314793150034],
    [126.93507098285538, 36.64210788827871],
    [127.50553754496315, 36.643447265652945]
]

# 변환 실행
result = converter.convert(rect_coords)

# 결과 출력
converter.show(result)

# GeoJSON 파일 생성
output_path = os.path.join(BASE_PATH, "static", "test_1.geojson")
converter.create_geojson(rect_coords, output_path, result=result)
```

## 핵심 기능: Rect2Region

`Rect2Region` 클래스는 사각형 영역을 한반도 행정구역으로 변환하는 핵심 기능을 제공합니다.

### 주요 메서드

#### 1. `convert(rect_coords, only_representive_text=False)`

사각형 영역에 포함되는 행정구역을 분석합니다.

**입력:**
- `rect_coords`: 4개의 좌표 리스트 `[[lon, lat], ...]`
- `only_representive_text`: True일 경우 대표 텍스트만 반환

**반환값:**
```python
{
    "representative": ["경기도 북부 포함", "충청북도 북부 포함"],  # 광역 단위 대표 표현
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
- 그 외: "강원도 북부 포함" (방향 기반)

#### 2. `convert_many(rect_coords_list, only_representive_text=False)`

여러 개의 사각형을 한 번에 변환합니다.

```python
rect_coords_list = [rect1, rect2, rect3]
results = converter.convert_many(rect_coords_list)
```

#### 3. `get_region_boundary(region_name)`

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

#### 4. `create_geojson(rect_coords, output_path, result=None, openbrowser=False)`

사각형과 포함된 행정구역을 GeoJSON 파일로 생성하고 GitHub에 푸시합니다.

```python
output_path = os.path.join(BASE_PATH, "static", "result.geojson")
converter.create_geojson(rect_coords, output_path, openbrowser=True)
```

**생성되는 GeoJSON 구조:**
- 입력 사각형 폴리곤
- 포함된 시/도 경계 폴리곤
- 각 시/도의 중심점

#### 5. `convert_json_file(input_file, output_file)`

JSON 파일의 `region_text` 필드를 변환합니다.

```python
using_data_path = os.path.join(BASE_PATH, "using_data")
input_file = os.path.join(using_data_path, "data.json")
output_file = os.path.join(using_data_path, "converted_data.json")
converter.convert_json_file(input_file, output_file)
```

### 사용 예시

```python
# main.py 참고
import config
from core.rect2region import Rect2Region

converter = Rect2Region()

# 테스트 케이스 1: 충청 지역
rect_coords = [
    [126.93167575079963, 37.10178611970895],
    [127.50557082786963, 37.10314793150034],
    [126.93507098285538, 36.64210788827871],
    [127.50553754496315, 36.643447265652945]
]

result = converter.convert(rect_coords)
converter.show(result)

# 출력:
# 중심 좌표: [127.2204..., 36.8724...]
# 광역 단위 대표 표현: ['경기도 남부 포함', '충청북도 북부 포함']
# 완전히 포함된 지역: ['천안시', '아산시', ...]
# 전체 지역 (완전+일부): ['천안시', '아산시', '평택시', ...]

# 테스트 케이스 2: 서울 전체
rect_coords_seoul = [
    [126.7, 37.7],
    [127.3, 37.7],
    [126.7, 37.4],
    [127.3, 37.4]
]

result2 = converter.convert(rect_coords_seoul)
# 광역 단위 대표 표현: ['서울특별시 전체']

# 테스트 케이스 3: 바다 한가운데 (범위 밖)
rect_coords_ocean = [
    [120.0, 35.0],
    [121.0, 35.0],
    [120.0, 34.0],
    [121.0, 34.0]
]

result3 = converter.convert(rect_coords_ocean)
# 가장 가까운 행정구역 정보 반환
```

## 프로젝트 구조

```
geo_map/
├── config.py                    # 환경 설정 (BASE_PATH 정의)
├── main.py                      # 메인 실행 예제
│
├── core/                        # 핵심 기능 모듈
│   ├── point2region.py          # 좌표 → 행정구역 변환
│   ├── rect2region.py           # 사각형 → 행정구역 변환 (핵심)
│   └── rect2geojson.py          # 사각형 → GeoJSON 변환
│
├── utils/                       # 유틸리티 모듈
│   ├── coord2region.py          # OSM shapefile 기반 지역 매칭 (geopandas 사용)
│   ├── check_shapefile.py       # Shapefile 검증 및 GeoJSON 변환
│   ├── add_center_coords.py    # GeoJSON에 중심좌표 추가
│   ├── test_distance.py         # 거리 계산 테스트
│   └── translate_regionname.py  # 지역명 번역 (LLM 활용)
│
├── src/
│   └── common_utils.py          # LLM API 호출 등 공통 유틸리티
│
├── using_data/                  # 행정구역 GeoJSON 데이터
│   ├── boundaries_KR_20220407.geojson
│   └── new_prk_admbnda_adm2_wfp_20190624.geojson
│
└── static/                      # 생성된 GeoJSON 파일 저장
```

## 활용 데이터 출처

모든 데이터는 위도 경도 좌표(EPSG:4326)로 구성되어 있습니다.

### 1. 북한 행정구역 데이터
- **출처**: [Humanitarian Data Exchange - North Korea Administrative Boundaries](https://data.humdata.org/dataset/cod-ab-prk)
- **내용**: 구, 군, 구역 수준의 북한 폴리곤 데이터
- **파일**: `new_prk_admbnda_adm2_wfp_20190624.geojson`

### 2. 대한민국 행정구역 데이터
- **출처**: [Humanitarian Data Exchange - South Korea Kontur Boundaries](https://data.humdata.org/dataset/kontur-boundaries-korea-republic-of)
- **내용**: 리 수준까지의 대한민국 폴리곤 데이터 (일부 지역)
- **파일**: `boundaries_KR_20220407.geojson`

### 3. 대한민국 상세 지역 데이터 (OSM)
- **출처**: [Geofabrik - South Korea](https://download.geofabrik.de/asia/south-korea.html)
- **내용**:
  - 대한민국 섬 지역 폴리곤 데이터
  - 거의 모든 "리" 수준까지의 포인트 데이터
- **용도**: 중심 좌표 참조 및 상세 지역 매칭

### 4. 북한 상세 지역 데이터 (OSM)
- **출처**: [Geofabrik - North Korea](https://download.geofabrik.de/asia/north-korea.html)
- **내용**:
  - 대한민국 섬 지역 폴리곤 데이터
  - 거의 모든 "리" 수준까지의 포인트 데이터
- **용도**: 북한 지역 중심 좌표 참조

### 행정구역 레벨
국 > 도/특별시/광역시 > 시/군/구/구역 > 읍/면/동 > 리/통/지구 > 반

## 의존성

주요 라이브러리:
- `shapely`: 지리 데이터 처리
- `geopandas`: Shapefile 처리 (utils 일부)
- `pandas`: 데이터 처리
