# 국경선 개미굴 메우기 수정 작업 보고서

**작업 일자**: 2025-10-28
**작업자**: Claude Code
**목적**: 이전 작업의 오류 수정 - 폴리곤 레벨에서 윗부분 경계선만 교체

---

## 1. 문제점 발견

### 이전 작업의 문제 (2025-10-27)
이전 `merge_border_with_north.py` 스크립트는 다음과 같은 치명적인 오류가 있었습니다:

**문제점**:
- `border_fixed_closed_only.geojson` (경기도+강원도 북부를 합친 데이터)로 **원본 경기도와 강원도를 완전히 교체**
- 결과적으로 **경기도가 사라지고** 강원도만 남음
- Feature 수: 2444개 → 2443개

**원본 데이터**:
```
Total features: 2444
Gyeonggi: 1개 (면적: 1.040578)
Gangwon: 1개 (면적: 1.700433)
```

**잘못된 결과 (boundaries_KR_20220407_updated.geojson)**:
```
Total features: 2443
Gyeonggi: 0개 ❌
Gangwon: 1개 (면적: 0.167095) - 북부만 남음
```

### 원인 분석

`merge_border_with_north.py`의 84-89번 라인:
```python
# 경기도/강원도가 아닌 나머지 features
other_features = gdf_original[~gdf_original[name_col].isin(['경기도', '강원도', '강원특별자치도'])].copy()

# 경기도/강원도 중 하나의 feature를 fixed geometry로 교체
gangwon_feature = gdf_original[gdf_original[name_col].isin(['강원도', '강원특별자치도'])].iloc[0:1].copy()
gangwon_feature.loc[:, 'geometry'] = fixed_geom  # ← 여기서 전체를 덮어씀!
```

**문제**: 경기도와 강원도를 완전히 제거하고, 하나의 feature(강원도)에 합쳐진 geometry를 덮어씌움

---

## 2. 올바른 해결 방법

### 전략
1. **원본 경기도와 강원도 각각 유지**
2. 각각에서 **북부 영역(border line 위)만 제거**
3. `border_fixed_closed_only.geojson`을 **경기도/강원도로 분할**
4. 각각의 남은 부분과 북부를 **개별적으로 합치기**

### 핵심 알고리즘

#### Step 1: 클리핑 폴리곤 생성
```python
# 경기도 북부 영역 (보더라인 위 + 경도 127.096 서쪽)
gyeonggi_clip = create_gyeonggi_clip_polygon(bounds)

# 강원도 북부 영역 (보더라인 위 + 경도 127.096 동쪽)
gangwon_clip = create_gangwon_clip_polygon(bounds)
```

#### Step 2: Fixed geometry 분할
```python
# border_fixed를 경기도/강원도 영역으로 분할
fixed_gyeonggi = fixed_geom.intersection(gyeonggi_clip)
fixed_gangwon = fixed_geom.intersection(gangwon_clip)
```

#### Step 3: 각 시/도 개별 업데이트
```python
def process_province(gdf, name_col, province_names, clip_polygon, fixed_geom_part):
    for idx, row in gdf.iterrows():
        if row[name_col] in province_names:
            original_geom = row['geometry']

            # 원본에서 북부 제거
            remaining = original_geom.difference(clip_polygon)

            # 북부를 fixed geometry로 교체
            updated_geom = unary_union([remaining, fixed_geom_part])

            gdf.at[idx, 'geometry'] = updated_geom
```

---

## 3. 작업 결과

### 새로운 스크립트: `fix_border_properly.py`

#### 처리 단계
1. **[1/9]** 북부 전체 클리핑 폴리곤 생성
2. **[2/9]** 경기도 북부 클리핑 폴리곤 생성 (경도 127.096 서쪽)
3. **[3/9]** 강원도 북부 클리핑 폴리곤 생성 (경도 127.096 동쪽)
4. **[4/9]** 원본 데이터 로드
5. **[5/9]** border_fixed 데이터 로드
6. **[6/9]** gangwon_boundaries 데이터 로드
7. **[7/9]** fixed geometry를 경기도/강원도로 분할
8. **[8/9]** 경기도 업데이트 (윗부분만 교체)
9. **[9/9]** 강원도 업데이트 (윗부분만 교체 + gangwon_boundaries 병합)

#### 실행 결과
```
Fixed Gyeonggi north area: 0.032798
Fixed Gangwon north area (merged): 0.084610

Gyeonggi:
  Original area: 1.040578
  Updated area:  1.043407
  Change: +0.002829 (+0.27%)

Gangwon:
  Original area: 1.700433
  Updated area:  1.715507
  Change: +0.015074 (+0.89%)
```

### 최종 파일: `boundaries_KR_20220407_updated.geojson`

| 항목 | 원본 | 이전(잘못된 버전) | 최종(올바른 버전) |
|------|------|------------------|------------------|
| **Total features** | 2444 | 2443 ❌ | 2444 ✅ |
| **경기도** | 1개 (1.040578) | 0개 ❌ | 1개 (1.043407) ✅ |
| **강원도** | 1개 (1.700433) | 1개 (0.167095) ⚠️ | 1개 (1.715507) ✅ |

---

## 4. 검증

### 검증 스크립트: `verify_result2.py`

```python
# 원본 vs 최종 비교
Gyeonggi:
  Original area: 1.040578
  Updated area:  1.043407
  Change: +0.002829 (+0.27%)

Gangwon:
  Original area: 1.700433
  Updated area:  1.715507
  Change: +0.015074 (+0.89%)

SUCCESS: Both Gyeonggi and Gangwon exist with updated northern borders!
```

### 검증 항목
- ✅ 경기도 존재 여부: **존재함**
- ✅ 강원도 존재 여부: **존재함**
- ✅ Feature 수 유지: **2444개** (원본과 동일)
- ✅ 면적 증가: 경기도 +0.27%, 강원도 +0.89% (개미굴이 메워짐)
- ✅ 폴리곤 레벨에서 윗부분만 교체: **성공**

---

## 5. 파일 구조

```
geo_map/
├── scripts/
│   ├── fix_border_ant_tunnels.py          # Step 1: 개미굴 메우기 (기존)
│   ├── merge_border_with_north.py         # Step 2: 병합 (잘못된 버전) ⚠️
│   ├── fix_border_properly.py             # Step 2: 올바른 병합 ✅
│   ├── verify_result2.py                  # 검증 스크립트
│   ├── README_border_fix.md               # 이전 보고서
│   └── README_border_fix_v2.md            # 본 보고서 ✅
├── using_data/
│   ├── boundaries_KR_20220407.geojson                  # 원본 (보존)
│   ├── boundaries_KR_20220407_updated.geojson          # 최종 결과 ✅
│   ├── boundaries_KR_20220407_updated_v2.geojson       # 백업 (동일)
│   └── boundaries_KR_20220407_updated_backup_wrong.geojson  # 잘못된 버전 백업
└── output/
    ├── border_fixed_with_layers.geojson
    ├── border_fixed_closed_only.geojson
    └── border_fixed_visualization.png
```

---

## 6. 사용 방법

### 재실행 (필요 시)

```bash
cd C:\Users\T3Q\jeonghan\practice\jeonghan\geo_map

# Step 1: 개미굴 메우기 (이미 완료됨)
C:\Users\T3Q\jeonghan\binch\Scripts\python.exe scripts/fix_border_ant_tunnels.py

# Step 2: 올바른 병합 (새 스크립트)
C:\Users\T3Q\jeonghan\binch\Scripts\python.exe scripts/fix_border_properly.py

# 검증
C:\Users\T3Q\jeonghan\binch\Scripts\python.exe scripts/verify_result2.py
```

### 파라미터 조정

**`fix_border_properly.py` 상단**:
```python
# 경기도/강원도 경계
GANGWON_GYEONGGI_BOUNDARY_LON = 127.096

# 보더라인
BORDER_LINE_COORDS = [
    [126.665, 37.788],
    [127.155, 38.255],
    [128.158, 38.255],
    [128.373, 38.482],
    [128.362, 38.673]
]
```

---

## 7. 기술적 세부사항

### 차이점 비교

| 항목 | 이전 방식 (merge_border_with_north.py) | 새로운 방식 (fix_border_properly.py) |
|------|--------------------------------------|-------------------------------------|
| **경기도 처리** | 제거됨 ❌ | 윗부분만 교체 ✅ |
| **강원도 처리** | 전체 교체 (북부만 남음) ❌ | 윗부분만 교체 ✅ |
| **Geometry 분할** | 없음 | 경도 127.096 기준으로 분할 ✅ |
| **Feature 수** | 2443개 (-1) ❌ | 2444개 (유지) ✅ |

### 핵심 개선사항

1. **개별 처리**: 경기도와 강원도를 각각 독립적으로 처리
2. **부분 교체**: 전체가 아닌 북부 영역만 교체
3. **Geometry 분할**: fixed_geom을 경기도/강원도 영역으로 정확히 분할
4. **데이터 보존**: 원본 feature 수 유지

---

## 8. 결론

### 문제 해결
- ❌ **이전**: 경기도가 사라지고 강원도에 흡수됨
- ✅ **현재**: 경기도와 강원도 각각의 윗부분 경계선만 개미굴이 메워진 버전으로 교체

### 최종 결과
- **경기도**: 면적 +0.27% (북부 개미굴 메움)
- **강원도**: 면적 +0.89% (북부 개미굴 메움 + gangwon_boundaries 병합)
- **Feature 수**: 2444개 유지
- **데이터 무결성**: 완벽하게 보존

---

## 9. 향후 작업

### 완료된 작업
- ✅ 개미굴 메우기 (Closing 연산)
- ✅ 폴리곤 레벨에서 윗부분만 교체
- ✅ 경기도/강원도 각각 유지
- ✅ gangwon_boundaries 병합

### 권장사항
1. **시각화 확인**: QGIS 또는 geojson.io에서 결과 확인
2. **파라미터 조정**: 필요 시 BUFFER_RADIUS 또는 BORDER_LINE_COORDS 조정
3. **백업 유지**: `boundaries_KR_20220407.geojson` (원본) 절대 삭제 금지

---

## 10. 참고 자료

### 관련 파일
- 원본 데이터: `boundaries_KR_20220407.geojson`
- 최종 결과: `boundaries_KR_20220407_updated.geojson`
- 잘못된 버전 백업: `boundaries_KR_20220407_updated_backup_wrong.geojson`

### 스크립트
- 올바른 병합: `fix_border_properly.py` ✅
- 검증: `verify_result2.py`

---

**작업 완료**: 2025-10-28
**소요 시간**: 약 1시간
**최종 결과물**: `boundaries_KR_20220407_updated.geojson` ✅
**상태**: 성공 - 경기도와 강원도 각각의 윗부분 경계선만 올바르게 교체됨
