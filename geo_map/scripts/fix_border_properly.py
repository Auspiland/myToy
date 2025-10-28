# -*- coding: utf-8 -*-
"""
국경선 개미굴 메우기 - 올바른 방법

문제점:
- 기존 스크립트는 경기도와 강원도를 완전히 교체해서 경기도가 사라짐

해결책:
1. 원본 경기도와 강원도 각각 유지
2. 각각에서 북부 영역(border line 위)만 제거
3. border_fixed_closed_only를 경기도/강원도로 분할
4. 각각의 남은 부분과 북부를 합치기
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import BASE_PATH
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, MultiPolygon, LineString
from shapely.ops import unary_union
from shapely.validation import make_valid


# 경로 설정
ORIGINAL_KR_PATH = os.path.join(BASE_PATH, "using_data", "boundaries_KR_20220407.geojson")
FIXED_BORDER_PATH = os.path.join(BASE_PATH, "output", "border_fixed_closed_only.geojson")
GANGWON_BOUNDARIES_PATH = os.path.join(BASE_PATH, "not_using_data", "gangwon_boundaries.geojson")
OUTPUT_PATH = os.path.join(BASE_PATH, "using_data", "boundaries_KR_20220407_updated_v2.geojson")

# 경기도/강원도 경계 (경도)
GANGWON_GYEONGGI_BOUNDARY_LON = 127.096

# 보더라인 (이 선 위쪽을 교체할 것)
BORDER_LINE_COORDS = [
    [126.66456778654037, 37.7881205935217],
    [127.15549185560224, 38.2552398658961],
    [128.15832162525874, 38.25483819709771],
    [128.37347632819063, 38.482391795333626],
    [128.3616636225412, 38.6730793098983]
]


def create_north_clip_polygon(bounds):
    """
    보더라인 북쪽 전체 영역을 나타내는 클리핑 폴리곤 생성

    Args:
        bounds: [minx, miny, maxx, maxy]

    Returns:
        Polygon representing area above border line
    """
    print("[1/9] Creating north clip polygon")

    # LineString 끝점을 bounds의 양 끝까지 확장
    extended_coords = [
        [bounds[0], BORDER_LINE_COORDS[0][1]],  # 왼쪽 확장
        *BORDER_LINE_COORDS,
        [bounds[2], BORDER_LINE_COORDS[-1][1]]  # 오른쪽 확장
    ]

    # 북쪽 클리핑 폴리곤 생성
    clip_coords = [
        *extended_coords,
        [bounds[2], bounds[3]],  # 우상단
        [bounds[0], bounds[3]]   # 좌상단
    ]
    clip_polygon = Polygon(clip_coords)

    if not clip_polygon.is_valid:
        clip_polygon = make_valid(clip_polygon)
        print("  Warning: clip_polygon was invalid, fixed")

    print(f"  Clip polygon area: {clip_polygon.area:.6f}")
    return clip_polygon


def create_gyeonggi_clip_polygon(bounds):
    """
    경기도 북부 영역만 나타내는 클리핑 폴리곤 (보더라인 위 + 경도 127.096 서쪽)
    """
    print("[2/9] Creating Gyeonggi north clip polygon")

    # 보더라인 중 경도 127.096 서쪽 부분만
    filtered_coords = [coord for coord in BORDER_LINE_COORDS if coord[0] < GANGWON_GYEONGGI_BOUNDARY_LON]

    if len(filtered_coords) == 0:
        # 첫 번째 점 사용
        filtered_coords = [BORDER_LINE_COORDS[0]]

    # 경계점 추가
    boundary_point = [GANGWON_GYEONGGI_BOUNDARY_LON, BORDER_LINE_COORDS[1][1]]

    clip_coords = [
        [bounds[0], filtered_coords[0][1]],  # 좌하단
        *filtered_coords,
        boundary_point,  # 경계점
        [GANGWON_GYEONGGI_BOUNDARY_LON, bounds[3]],  # 우상단
        [bounds[0], bounds[3]]  # 좌상단
    ]

    clip_polygon = Polygon(clip_coords)

    if not clip_polygon.is_valid:
        clip_polygon = make_valid(clip_polygon)

    print(f"  Gyeonggi clip polygon area: {clip_polygon.area:.6f}")
    return clip_polygon


def create_gangwon_clip_polygon(bounds):
    """
    강원도 북부 영역만 나타내는 클리핑 폴리곤 (보더라인 위 + 경도 127.096 동쪽)
    """
    print("[3/9] Creating Gangwon north clip polygon")

    # 보더라인 중 경도 127.096 동쪽 부분만
    filtered_coords = [coord for coord in BORDER_LINE_COORDS if coord[0] >= GANGWON_GYEONGGI_BOUNDARY_LON]

    if len(filtered_coords) == 0:
        filtered_coords = BORDER_LINE_COORDS[-3:]

    # 경계점
    boundary_point = [GANGWON_GYEONGGI_BOUNDARY_LON, BORDER_LINE_COORDS[1][1]]

    clip_coords = [
        boundary_point,  # 경계점
        *filtered_coords,
        [bounds[2], filtered_coords[-1][1]],  # 우하단
        [bounds[2], bounds[3]],  # 우상단
        [GANGWON_GYEONGGI_BOUNDARY_LON, bounds[3]]  # 좌상단
    ]

    clip_polygon = Polygon(clip_coords)

    if not clip_polygon.is_valid:
        clip_polygon = make_valid(clip_polygon)

    print(f"  Gangwon clip polygon area: {clip_polygon.area:.6f}")
    return clip_polygon


def process_province(gdf, name_col, province_names, clip_polygon, fixed_geom_part):
    """
    특정 시/도의 북부를 교체

    Args:
        gdf: 원본 GeoDataFrame
        name_col: 시/도 이름 컬럼
        province_names: 시/도 이름 리스트 (예: ['경기도'])
        clip_polygon: 북부 영역 클리핑 폴리곤
        fixed_geom_part: 교체할 북부 geometry

    Returns:
        업데이트된 GeoDataFrame
    """
    province_name_str = " or ".join(province_names)
    print(f"[Processing] {province_name_str}")

    updated = False

    for idx, row in gdf.iterrows():
        if row[name_col] in province_names:
            original_geom = row['geometry']

            # 원본에서 북부 제거
            remaining = original_geom.difference(clip_polygon)

            # 북부를 fixed geometry로 교체
            updated_geom = unary_union([remaining, fixed_geom_part])

            if not updated_geom.is_valid:
                updated_geom = make_valid(updated_geom)

            gdf.at[idx, 'geometry'] = updated_geom
            updated = True

            print(f"  Updated: {row[name_col]}")
            print(f"    Original area: {original_geom.area:.6f}")
            print(f"    Updated area: {updated_geom.area:.6f}")
            break

    if not updated:
        print(f"  Warning: {province_name_str} not found")

    return gdf


def main():
    print("=" * 80)
    print("국경선 개미굴 메우기 - 올바른 버전")
    print("=" * 80)
    print("전략: 경기도와 강원도 각각의 윗부분 경계선만 교체")
    print()

    # 1. 원본 데이터 로드
    print("[4/9] Loading original data")
    gdf_original = gpd.read_file(ORIGINAL_KR_PATH)

    # name 필드 찾기
    name_fields = ['name', 'name_ko', 'NAME', 'ADM_NM', 'ADM1_KO', 'ADM1_NAME']
    name_col = None
    for field in name_fields:
        if field in gdf_original.columns:
            name_col = field
            break

    if name_col is None:
        raise ValueError("Name field not found")

    print(f"  Using name field: {name_col}")
    print(f"  Total features: {len(gdf_original)}")

    # 2. border_fixed 데이터 로드
    print("[5/9] Loading border_fixed data")
    gdf_fixed = gpd.read_file(FIXED_BORDER_PATH)

    if 'layer' in gdf_fixed.columns:
        fixed_geom = gdf_fixed[gdf_fixed['layer'] == 'closed'].geometry.iloc[0]
    else:
        fixed_geom = gdf_fixed.geometry.iloc[0]

    print(f"  Fixed border area: {fixed_geom.area:.6f}")

    # 3. gangwon_boundaries 데이터 로드 및 병합
    print("[6/9] Loading gangwon_boundaries data")
    gdf_gangwon_boundaries = gpd.read_file(GANGWON_BOUNDARIES_PATH)
    gangwon_boundaries_geom = unary_union(gdf_gangwon_boundaries.geometry)
    print(f"  Gangwon boundaries area: {gangwon_boundaries_geom.area:.6f}")

    # 4. bounds 계산
    bounds = gdf_original.total_bounds

    # 5. 클리핑 폴리곤 생성
    north_clip = create_north_clip_polygon(bounds)
    gyeonggi_clip = create_gyeonggi_clip_polygon(bounds)
    gangwon_clip = create_gangwon_clip_polygon(bounds)

    # 6. fixed_geom을 경기도/강원도로 분할
    print("[7/9] Splitting fixed geometry into Gyeonggi/Gangwon parts")
    fixed_gyeonggi = fixed_geom.intersection(gyeonggi_clip)
    fixed_gangwon_original = fixed_geom.intersection(gangwon_clip)

    # 강원도 북부에 gangwon_boundaries 합치기
    gangwon_boundaries_north = gangwon_boundaries_geom.intersection(gangwon_clip)
    fixed_gangwon = unary_union([fixed_gangwon_original, gangwon_boundaries_north])

    if not fixed_gangwon.is_valid:
        fixed_gangwon = make_valid(fixed_gangwon)

    print(f"  Fixed Gyeonggi north area: {fixed_gyeonggi.area:.6f}")
    print(f"  Fixed Gangwon north area (original): {fixed_gangwon_original.area:.6f}")
    print(f"  Gangwon boundaries north area: {gangwon_boundaries_north.area:.6f}")
    print(f"  Fixed Gangwon north area (merged): {fixed_gangwon.area:.6f}")

    # 7. 경기도 업데이트
    print("[8/9] Updating Gyeonggi")
    gdf_updated = process_province(
        gdf_original.copy(),
        name_col,
        ['경기도'],
        gyeonggi_clip,
        fixed_gyeonggi
    )

    # 8. 강원도 업데이트
    print("[8/9] Updating Gangwon")
    gdf_updated = process_province(
        gdf_updated,
        name_col,
        ['강원도', '강원특별자치도'],
        gangwon_clip,
        fixed_gangwon
    )

    # 9. 저장
    print(f"[9/9] Saving updated GeoJSON: {OUTPUT_PATH}")
    gdf_updated.to_file(OUTPUT_PATH, driver="GeoJSON")
    print(f"  Saved {len(gdf_updated)} features")

    # 10. 검증
    print("\n=== Verification ===")
    gyeonggi = gdf_updated[gdf_updated[name_col] == '경기도']
    gangwon = gdf_updated[gdf_updated[name_col].isin(['강원도', '강원특별자치도'])]

    print(f"Gyeonggi exists: {len(gyeonggi) > 0}")
    print(f"Gangwon exists: {len(gangwon) > 0}")

    if len(gyeonggi) > 0:
        print(f"Gyeonggi area: {gyeonggi.geometry.iloc[0].area:.6f}")
    if len(gangwon) > 0:
        print(f"Gangwon area: {gangwon.geometry.iloc[0].area:.6f}")

    print()
    print("=" * 80)
    print("완료! (Completed)")
    print("=" * 80)
    print(f"Updated GeoJSON saved to: {OUTPUT_PATH}")
    print()
    print("작업 내용:")
    print("  1. 경기도의 윗부분 경계선만 개미굴 메워진 버전으로 교체")
    print("  2. 강원도의 윗부분 경계선만 개미굴 메워진 버전으로 교체")
    print("  3. 강원도 북부는 gangwon_boundaries와도 합집합")
    print("  4. 경기도와 강원도 모두 유지됨")


if __name__ == "__main__":
    main()
