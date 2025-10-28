# Scripts 디렉토리 문서

이 디렉토리는 한국 행정구역 경계(GeoJSON) 데이터 처리를 위한 스크립트들을 포함합니다.  
독립적인 변환 및 테스트 코드로 구성되어 있습니다.  
이미 실행된 후 저장되어 있습니다.

## 공통 설정

대부분의 스크립트는 `config.py`의 `BASE_PATH`를 사용하여 절대 경로를 기반으로 작동합니다.

```python
from config import BASE_PATH
```

---

## 유틸리티 스크립트

### coord2region.py

#### 기능
좌표(사각형 영역)로부터 해당 지역의 행정구역명을 찾는 유틸리티

#### 주요 기능
1. **list_regions_in_center_box()**: 사각형 중앙 박스 내 도시/군/구 목록 추출
2. **get_representative_region()**: 대표 지역명 하나 추출 (면적 교집합 우선)
3. **지역명 정규화**: 행정단위 접미사 제거, 다국어 표기 처리
4. **상위 지역 매핑**: CSV 파일 기반 시도/시군구/읍면동 계층 구조 매핑

#### 입력
- Shapefile: `south-korea-251021-free.shp`, `north-korea-251021-free.shp`
- CSV: `SGIS 행정구역 코드202406.csv`, `통계청_원격탐사_북한행정지역_20210826.csv`

#### 반환
- GeoDataFrame: 중심 박스 내 지역 목록 (거리순 정렬)
- Dict: 대표 지역 정보 (이름, 타입, 면적, 상위 지역 등)

---

### check_shapefile.py

#### 기능
Shapefile 탐색, 변환, 정보 출력 유틸리티

#### 주요 함수
1. **list_shp_files()**: 디렉토리 내 모든 .shp 파일 재귀 검색
2. **print_boundaries()**: 경계 좌표 출력 (미리보기/전체)
3. **convert2json()**: Shapefile → GeoJSON 변환
4. **print_infos_dir()**: fclass별 통계 및 인구 정보 출력
5. **describe_shapefile()**: 파일 메타데이터 요약 (CRS, 컬럼, 범위 등)

#### 사용 예시
```python
describe_shapefile(filepath)  # 단일 파일 정보
convert2json_dir(DIR)         # 디렉토리 일괄 변환
```

---

### add_center_coords.py

#### 기능
GeoJSON 파일에 중심 좌표(center_lon, center_lat) 추가

#### 알고리즘
1. 중심 좌표 참조 파일(`kr/kp_gis_osm_places_free_1.geojson`)에서 이름별 좌표 로딩
2. 각 feature의 이름으로 중심 좌표 조회
3. 없으면 geometry의 centroid 계산
4. properties에 center_lon, center_lat 추가

#### 입력
- `boundaries_KR_20220407.geojson`
- `new_prk_admbnda_adm2_wfp_20190624.geojson`

#### 출력
- 동일 파일에 덮어쓰기 (in-place update)

---

### test_distance.py

#### 기능
좌표로부터 가장 가까운 행정구역(구/군/구역) 찾기 테스트

#### 알고리즘
1. 대한민국 + 북한 GeoJSON에서 구/군/구역 단위 추출
2. 테스트 좌표에서 각 경계까지 최단 거리 계산 (Haversine formula)
3. 거리순 정렬하여 가장 가까운 5개 출력

#### 사용 예시
```python
test_lon, test_lat = 127.5000, 43.3000  # 테스트 좌표
# 출력: 가장 가까운 5개 행정구역 + 거리(km)
```

---

### translate_regionname.py

#### 기능
북한 GeoJSON의 영문 지명을 LLM으로 한국어 번역

#### 주요 기능
1. **collect_unique_names()**: ADM0_EN/ADM1_EN/ADM2_EN 영어 지명 수집
2. **translate_names_with_llm()**: GPT API로 일괄 번역
3. **insert_ko_and_prune()**: ADM0_KO/ADM1_KO/ADM2_KO 삽입, 불필요 키 제거
4. **apply_fix_table()**: 번역 오류 수동 수정 (장도군→창도군 등)

#### 입력
- `prk_admbnda_adm2_wfp_20190624.geojson`

#### 출력
- `new_prk_admbnda_adm2_wfp_20190624.geojson`

#### 주의사항
- GPT API 키 필요 (`src.common_utils.response_GPT`)
- 번역 결과는 수동 검증 권장

---

### update_polygon.py

#### 기능
V-World API를 사용하여 행정구역 경계(geometry) 업데이트

#### 알고리즘
1. admin_level 4 지역(시도) 추출
2. 중심 좌표에서 V-World API 호출
3. 실패 시 대한민국 중심 방향으로 좌표 조정하며 최대 9회 재시도
4. 성공한 geometry로 업데이트

#### 입력
- `boundaries_KR_20220407.geojson`

#### 출력
- `boundaries_KR_20220407_updated.geojson`

#### 주요 파라미터
- `V_WORLD_API_KEY`: 환경 변수 필요
- `TARGET_REGION`: 특정 지역만 업데이트 (None=전체)

---

### update_center_coords.py

#### 기능
admin_level 4 지역의 중심 좌표 계산 및 whole.geojson 생성

#### 알고리즘
1. 각 지역의 geometry에서 centroid 계산
2. 인천광역시는 하드코딩 값 사용 (섬 때문에 centroid가 부정확)
3. 원본 파일에 center_lon/center_lat 추가
4. whole.geojson 생성: Polygon + 중심점 Point features

#### 입력
- `boundaries_KR_20220407_updated.geojson`

#### 출력
- `boundaries_KR_20220407_updated_updated.geojson` (중심 좌표 추가)
- `whole.geojson`: Polygon + Point features

#### 특별 처리
- 인천광역시: `(126.6176012, 37.4792081)` 하드코딩

---

## 경계 데이터 처리 파이프라인

---

## 1. fix_border_ant_tunnels.py

### 기능
국경선(경기도/강원도 북부)의 불필요하게 복잡하고 좁은 협곡(개미굴)을 메우는 스크립트

### 알고리즘
1. WGS84 → EPSG:5179 좌표계 변환 (미터 단위)
2. 경기도/강원도 추출
3. 사용자 정의 LineString 북쪽 영역 필터링
4. **Morphological Closing 연산**: buffer(+r) → buffer(-r)
5. 내부 구멍(holes) 제거
6. 추가된 면적 계산

### 입력
- `using_data/boundaries_KR_20220407.geojson`: 원본 경계 데이터

### 출력
- `output/border_fixed_with_layers.geojson`: 원본/처리/추가 레이어 포함
- `output/border_fixed_closed_only.geojson`: Closing 결과만
- `output/border_fixed_visualization.png`: 시각화 이미지

### 파라미터
- `BUFFER_RADIUS`: 100m (약 200m 폭 협곡 메움)
- `TARGET_PROVINCES`: ["경기도", "강원도", "강원특별자치도"]
- `BORDER_LINE_COORDS`: 처리 경계선 좌표

---

## 2. merge_border_with_north.py

### 기능
개미굴 메운 경계와 강원도 북부 영역을 원본 데이터에 병합

### 알고리즘
1. `border_fixed_closed_only.geojson`를 원본에 병합
2. 강원도만 추출
3. 강원도 북부 영역(보더라인 위 + 경도 127.096 동쪽) 클리핑
4. `gangwon_boundaries.geojson`의 해당 영역과 합집합
5. 강원도 업데이트 후 저장

### 입력
- `output/border_fixed_closed_only.geojson`: 개미굴 메운 경계
- `not_using_data/gangwon_boundaries.geojson`: 강원도 추가 경계
- `using_data/boundaries_KR_20220407.geojson`: 원본 데이터

### 출력
- `using_data/boundaries_KR_20220407_updated.geojson`: 업데이트된 경계

### 주요 상수
- `GANGWON_GYEONGGI_BOUNDARY_LON`: 127.096 (강원/경기 경계 경도)
- `BORDER_LINE_COORDS`: 보더라인 좌표

---

## 3. fix_border_properly.py

### 기능
경기도와 강원도 각각의 북부 경계선만 올바르게 교체 (v2)

### 알고리즘
1. 원본에서 경기도/강원도 각각 유지
2. 각각에서 북부 영역(border line 위)만 제거
3. `border_fixed_closed_only`를 경기도/강원도로 분할
4. 각각의 남은 부분과 북부를 합치기
5. 강원도 북부에 `gangwon_boundaries` 합집합

### 입력
- `using_data/boundaries_KR_20220407.geojson`: 원본
- `output/border_fixed_closed_only.geojson`: 개미굴 메운 경계
- `not_using_data/gangwon_boundaries.geojson`: 강원도 추가 경계

### 출력
- `using_data/boundaries_KR_20220407_updated_v2.geojson`: 올바르게 업데이트된 경계

### 특징
- 경기도가 사라지지 않도록 각각 독립적으로 처리
- 경기도/강원도 클리핑 영역 분리

---

## 4. verify_result2.py

### 기능
원본, 업데이트(v1), 업데이트(v2) 파일 비교 및 검증

### 알고리즘
1. 세 파일 로드
2. 경기도/강원도 존재 여부 확인
3. 면적 변화 분석 및 출력

### 입력
- `using_data/boundaries_KR_20220407.geojson`: 원본
- `using_data/boundaries_KR_20220407_updated.geojson`: v1 (경기도 누락)
- `using_data/boundaries_KR_20220407_updated_v2.geojson`: v2 (정상)

### 출력
- 콘솔 출력: 각 파일의 경기도/강원도 상태 및 면적

---

## 5. process_boundaries_v2.py

### 기능
경기도/강원도 경계선에서 특정 구간 추출 및 연결

### 알고리즘
1. 강원도/경기도 경계 다각형에서 모든 좌표 추출
2. 유클리드 거리로 시작/끝점에 가장 가까운 인덱스 찾기
3. 두 경로(직선/둘레) 중 짧은 경로 선택
4. 사용자 제공 LineString과 연결
5. 최종 연결선 GeoJSON 생성

### 입력
- `using_data/boundaries_KR_20220407_updated.geojson`
- 하드코딩된 시작/끝점 좌표
- 하드코딩된 연결선 좌표

### 출력
- `output/connected_line_v2.geojson`: 연결된 LineString

### 주요 함수
- `distance()`: 유클리드 거리 계산
- `find_closest_point_index()`: 최근접 점 찾기
- `extract_line_between_points()`: 경계선 구간 추출

---

## 6. apply_right_hand_rule.py

### 기능
GeoJSON Polygon/MultiPolygon에 Right-Hand Rule 적용

### 알고리즘
1. Shoelace formula로 다각형 signed area 계산
2. Outer ring: 반시계 방향(CCW, 양수 면적) 강제
3. Inner ring (holes): 시계 방향(CW, 음수 면적) 강제
4. 닫히지 않은 ring 자동 닫기

### 입력
- `static/whole.geojson`

### 출력
- 동일 파일에 덮어쓰기 (in-place update)

### 주요 함수
- `calculate_polygon_area()`: signed area 계산
- `ensure_ring_closed()`: ring 닫기
- `apply_right_hand_rule()`: 좌표 순서 조정

---

## 7. replace_boundaries_v4.py

### 기능
강원도/경기도 경계선의 특정 구간을 연결선으로 교체

### 알고리즘
1. `connected_line_v2.geojson` 로드
2. 강원도/경기도 각각 MultiPolygon의 largest polygon 찾기
3. 시작/끝점 사이의 **짧은 경로** 선택 및 교체
4. 경기도: 경계 근처 inner rings(holes) 제거
5. 경기도: 경계 근처 작은 polygon 제거 (반경 0.05도 이내)

### 입력
- `using_data/boundaries_KR_20220407_updated.geojson`
- `output/connected_line_v2.geojson`

### 출력
- `using_data/boundaries_KR_20220407_modified.geojson`

### 주요 함수
- `get_largest_polygon_index()`: MultiPolygon에서 최대 polygon 찾기
- `replace_boundary_section()`: 경계 구간 교체 (짧은 경로 선택)
- `remove_small_polygons_near_boundary()`: 경계 근처 작은 polygon 제거

---

## 8. show_all_geojson.py

### 기능
admin_level 4 지역을 필터링하여 whole.geojson 생성

### 알고리즘
1. `boundaries_KR_20220407_modified.geojson` 로드
2. admin_level == 4인 feature만 필터링
3. (옵션) 특정 지역만 선택 (REGION_OPTION)
4. Polygon/MultiPolygon features 추가
5. 각 지역의 중심점(Point) features 생성 및 추가

### 입력
- `using_data/boundaries_KR_20220407_modified.geojson`

### 출력
- `static/whole.geojson`: Polygon + Point features

### 옵션
- `REGION_OPTION = None`: 모든 지역 (기본값)
- `REGION_OPTION = ["경기도", "강원도"]`: 특정 지역만

---

---

## 전체 파이프라인 실행된 순서

### 경계 처리 파이프라인
```
1. fix_border_ant_tunnels.py         # 개미굴 메우기
2. fix_border_properly.py            # 경기도/강원도 경계 올바르게 교체
3. verify_result2.py                 # 결과 검증
4. process_boundaries_v2.py          # 경계선 구간 추출
5. replace_boundaries_v4.py          # 경계선 교체
6. apply_right_hand_rule.py          # Right-hand rule 적용
7. show_all_geojson.py               # 최종 GeoJSON 생성
```

### 유틸리티 스크립트 (독립 실행)
- `coord2region.py`: 좌표→지역명 변환 테스트
- `check_shapefile.py`: Shapefile 검사/변환
- `add_center_coords.py`: 중심 좌표 일괄 추가
- `test_distance.py`: 거리 계산 테스트
- `translate_regionname.py`: 북한 지명 번역
- `update_polygon.py`: V-World API로 경계 업데이트
- `update_center_coords.py`: 중심 좌표 계산 및 whole.geojson 생성

---

## 버전 히스토리

### v2 (2025-10-28)

#### 주요 개선사항

**1. 코드 품질 향상**
- 하드코딩된 경로 제거: `update_polygon.py`, `update_center_coords.py`를 `BASE_PATH` 기반으로 변경
- 매직 넘버 제거: 상수를 `common_constants.py`로 분리
- 로깅 시스템 도입: `print()` → `logging` 모듈로 전면 교체

**2. 공통 모듈화**
- `common_constants.py` 생성: 파이프라인 전체에서 사용하는 공통 상수 통합
  - `BORDER_LINE_COORDS`, `KR_CENTER_LON/LAT`, `INCHEON_HARDCODED` 등
  - 중복 코드 제거 및 일관성 확보

**3. 에러 핸들링 개선**
- `traceback` 모듈 추가: 상세한 에러 정보 출력
- API 키 검증: `update_polygon.py`에서 `.env` 파일 누락 시 명확한 에러 메시지

**4. 버그 수정**
- `coord2region.py:237`: None 딕셔너리 안전 처리
- `update_center_coords.py:72`: `.geojson` 중복 생성 방지
- `translate_regionname.py:46`: 중첩 JSON 중괄호 올바른 파싱

**5. 테스트 코드 분리**
- `test_coord2region.py` 생성: 테스트 코드를 별도 파일로 분리

**6. 매개변수 검증**
- `coord2region.py`의 `list_regions_in_center_box()`: 입력값 검증 로직 추가

**7. API 개선**
- `update_polygon.py`: V-World API 재시도 로직 개선
- 환경 변수 경로를 BASE_PATH 기반으로 안전하게 처리

#### 파일 변경 사항
- 신규: `common_constants.py` - 공통 상수 모듈
- 신규: `test_coord2region.py` - coord2region 테스트 스크립트
- 수정: `update_polygon.py`, `update_center_coords.py`, `check_shapefile.py`, `coord2region.py`, `translate_regionname.py`

---

## 주의사항

1. 모든 스크립트는 `config.py`의 `BASE_PATH`를 사용합니다.
2. 일부 스크립트는 하드코딩된 좌표를 사용하므로 수정 시 주의 필요.
3. 경로 변경 시 절대 경로 대신 `os.path.join(BASE_PATH, ...)`를 사용하세요.
4. GeoJSON 파일은 UTF-8 인코딩을 사용합니다.
5. Shapely validation 에러 시 `make_valid()` 자동 적용됩니다.

---

## 디버깅

각 스크립트는 실행 중 자세한 로그를 출력합니다:
- 파일 로딩 상태
- 처리 단계별 진행 상황
- Geometry 면적 정보
- 에러 및 경고 메시지

문제 발생 시 콘솔 출력을 확인하여 어느 단계에서 실패했는지 파악할 수 있습니다.
