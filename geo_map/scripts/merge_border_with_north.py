# -*- coding: utf-8 -*-
"""
국경선 개미굴 메우기 + 강원도 북부 합집합 최종 병합

작업 순서:
1. border_fixed_closed_only.geojson (개미굴 메워진 경기도+강원도)를 원본에 병합
2. 병합된 데이터에서 강원도만 추출
3. 강원도 북부 영역(보더라인 위 + 경도 127.096 동쪽)만 클리핑
4. gangwon_boundaries.geojson의 해당 영역과 합집합
5. 강원도 업데이트 후 updated 파일로 저장
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import BASE_PATH
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, MultiPolygon, LineString, mapping
from shapely.ops import unary_union
from shapely.validation import make_valid
import json


# 경로 설정
FIXED_BORDER_PATH = os.path.join(BASE_PATH, "output", "border_fixed_closed_only.geojson")
GANGWON_BOUNDARIES_PATH = os.path.join(BASE_PATH, "not_using_data", "gangwon_boundaries.geojson")
ORIGINAL_KR_PATH = os.path.join(BASE_PATH, "using_data", "boundaries_KR_20220407.geojson")
OUTPUT_PATH = os.path.join(BASE_PATH, "using_data", "boundaries_KR_20220407_updated.geojson")

# 경기도/강원도 경계 (이 경도 동쪽이 강원도)
GANGWON_GYEONGGI_BOUNDARY_LON = 127.096
GANGWON_GYEONGGI_BOUNDARY_LAT = 38.281

# 보더라인 (아까 사용한 LineString)
BORDER_LINE_COORDS = [
    [126.66456778654037, 37.7881205935217],
    [127.15549185560224, 38.2552398658961],
    [128.15832162525874, 38.25483819709771],
    [128.37347632819063, 38.482391795333626],
    [128.3616636225412, 38.6730793098983]
]


def merge_fixed_border_to_original(original_path, fixed_path):
    """
    1단계: border_fixed_closed_only를 원본 데이터에 병합.
    경기도와 강원도를 개미굴 메워진 버전으로 교체.
    """
    print("[1/8] Merging border_fixed_closed_only to original")

    # 원본 로드
    gdf_original = gpd.read_file(original_path)

    # 개미굴 메워진 데이터 로드
    gdf_fixed = gpd.read_file(fixed_path)

    # name 필드 찾기
    name_fields = ['name', 'name_ko', 'NAME', 'ADM_NM', 'ADM1_KO', 'ADM1_NAME']
    name_col = None
    for field in name_fields:
        if field in gdf_original.columns:
            name_col = field
            break

    if name_col is None:
        raise ValueError("Name field not found in original GeoJSON")

    print(f"  Using name field: {name_col}")

    # fixed 데이터의 geometry 추출
    if 'layer' in gdf_fixed.columns:
        fixed_geom = gdf_fixed[gdf_fixed['layer'] == 'closed'].geometry.iloc[0]
    else:
        fixed_geom = gdf_fixed.geometry.iloc[0]

    print(f"  Fixed border area: {fixed_geom.area:.6f}")

    # 경기도/강원도를 fixed geometry로 교체
    # 전략: 원본에서 경기도/강원도를 제거하고 fixed geometry를 추가

    # 1. 경기도/강원도가 아닌 나머지 features
    other_features = gdf_original[~gdf_original[name_col].isin(['경기도', '강원도', '강원특별자치도'])].copy()

    # 2. 경기도/강원도 중 하나의 feature를 fixed geometry로 교체
    gangwon_feature = gdf_original[gdf_original[name_col].isin(['강원도', '강원특별자치도'])].iloc[0:1].copy()
    gangwon_feature.loc[:, 'geometry'] = fixed_geom

    # 3. 병합 (경기도는 제거됨, 강원도에 합쳐짐)
    gdf_merged = gpd.GeoDataFrame(
        pd.concat([other_features, gangwon_feature], ignore_index=True),
        crs=gdf_original.crs
    )

    print(f"  Merged GeoDataFrame: {len(gdf_merged)} features")
    return gdf_merged, name_col


def create_gangwon_north_clip_polygon():
    """
    강원도 북부 영역만 추출하기 위한 클리핑 폴리곤 생성.
    - 보더라인 위쪽
    - 경도 127.096 동쪽
    """
    print("[2/8] Creating Gangwon north clip polygon")

    # 보더라인 중 경도 127.096 이상 부분만 추출
    filtered_coords = [coord for coord in BORDER_LINE_COORDS if coord[0] >= GANGWON_GYEONGGI_BOUNDARY_LON]

    if len(filtered_coords) == 0:
        raise ValueError("No border line coords found east of 127.096")

    # 시작점 추가 (경계점)
    start_point = [GANGWON_GYEONGGI_BOUNDARY_LON, GANGWON_GYEONGGI_BOUNDARY_LAT]

    # 클리핑 폴리곤 좌표 생성
    max_lon = 129.0
    max_lat = 39.0

    clip_coords = [
        start_point,
        *filtered_coords,
        [filtered_coords[-1][0], max_lat],  # 우상단
        [max_lon, max_lat],  # 최우상단
        [max_lon, start_point[1]],  # 우하단
        start_point  # 닫기
    ]

    clip_polygon = Polygon(clip_coords)

    if not clip_polygon.is_valid:
        clip_polygon = make_valid(clip_polygon)
        print("  Warning: clip_polygon was invalid, fixed")

    print(f"  Clip polygon area: {clip_polygon.area:.6f}")
    return clip_polygon


def extract_gangwon_from_merged(gdf_merged, name_col):
    """병합된 데이터에서 강원도 geometry 추출"""
    print("[3/8] Extracting Gangwon from merged data")

    gangwon_row = gdf_merged[gdf_merged[name_col].isin(['강원도', '강원특별자치도'])]

    if len(gangwon_row) == 0:
        raise ValueError("Gangwon not found in merged data")

    gangwon_geom = gangwon_row.geometry.iloc[0]
    print(f"  Gangwon area: {gangwon_geom.area:.6f}")

    return gangwon_geom


def load_and_clip_gangwon_boundaries(gangwon_path, clip_polygon):
    """gangwon_boundaries.geojson에서 같은 영역 추출"""
    print(f"[4/8] Loading gangwon_boundaries and clipping: {gangwon_path}")
    gdf = gpd.read_file(gangwon_path)

    if len(gdf) == 0:
        raise ValueError("Gangwon boundaries GeoJSON is empty")

    # 전체 geometry 합치기
    gangwon_geom = unary_union(gdf.geometry)

    # 클리핑
    clipped_geom = gangwon_geom.intersection(clip_polygon)

    print(f"  Clipped area: {clipped_geom.area:.6f}")
    return clipped_geom


def clip_gangwon_north(gangwon_geom, clip_polygon):
    """강원도에서 북부 영역만 클리핑"""
    print("[5/8] Clipping Gangwon north region")

    clipped = gangwon_geom.intersection(clip_polygon)
    print(f"  Clipped Gangwon north area: {clipped.area:.6f}")

    return clipped


def merge_geometries(geom1, geom2):
    """두 geometry 합집합"""
    print(f"[6/8] Merging two geometries")

    merged = unary_union([geom1, geom2])

    if not merged.is_valid:
        merged = make_valid(merged)
        print("  Warning: Merged geometry was invalid, fixed")

    print(f"  Merged area: {merged.area:.6f}")
    return merged


def update_gangwon_in_gdf(gdf_merged, name_col, clip_polygon, merged_north_geom):
    """
    병합된 GeoDataFrame에서 강원도를 최종 업데이트.

    전략:
    1. 강원도에서 클리핑 영역 제거
    2. 합쳐진 북부 영역 추가
    """
    print("[7/8] Updating Gangwon in merged GeoDataFrame")

    updated = False

    for idx, row in gdf_merged.iterrows():
        province_name = row[name_col]

        if province_name in ["강원도", "강원특별자치도"]:
            current_gangwon = row['geometry']

            # 현재 강원도에서 클리핑 영역 제거
            remaining_gangwon = current_gangwon.difference(clip_polygon)

            # 합쳐진 북부 영역 추가
            updated_gangwon = unary_union([remaining_gangwon, merged_north_geom])

            if not updated_gangwon.is_valid:
                updated_gangwon = make_valid(updated_gangwon)

            gdf_merged.at[idx, 'geometry'] = updated_gangwon
            updated = True
            print(f"  Updated: {province_name}")
            print(f"    Before area: {current_gangwon.area:.6f}")
            print(f"    After area: {updated_gangwon.area:.6f}")
            break

    if not updated:
        raise ValueError("Gangwon not found in merged GeoDataFrame")

    return gdf_merged


def main():
    print("=" * 80)
    print("국경선 개미굴 메우기 + 강원도 북부 합집합 최종 병합")
    print("=" * 80)
    print(f"Gangwon/Gyeonggi boundary: lon={GANGWON_GYEONGGI_BOUNDARY_LON}, lat={GANGWON_GYEONGGI_BOUNDARY_LAT}")
    print()

    # 1단계: border_fixed_closed_only를 원본에 병합
    gdf_merged, name_col = merge_fixed_border_to_original(ORIGINAL_KR_PATH, FIXED_BORDER_PATH)

    # 2단계: 클리핑 폴리곤 생성
    clip_polygon = create_gangwon_north_clip_polygon()

    # 3단계: 병합된 데이터에서 강원도 추출
    gangwon_geom = extract_gangwon_from_merged(gdf_merged, name_col)

    # 4단계: gangwon_boundaries에서 북부 영역 추출
    gangwon_boundaries_north = load_and_clip_gangwon_boundaries(GANGWON_BOUNDARIES_PATH, clip_polygon)

    # 5단계: 강원도 북부만 클리핑
    gangwon_north = clip_gangwon_north(gangwon_geom, clip_polygon)

    # 6단계: 두 geometry 합집합
    merged_north = merge_geometries(gangwon_north, gangwon_boundaries_north)

    # 7단계: 강원도 최종 업데이트
    gdf_final = update_gangwon_in_gdf(gdf_merged, name_col, clip_polygon, merged_north)

    # 8단계: 저장
    print(f"[8/8] Saving final GeoJSON: {OUTPUT_PATH}")
    gdf_final.to_file(OUTPUT_PATH, driver="GeoJSON")
    print(f"  Saved {len(gdf_final)} features")

    print()
    print("=" * 80)
    print("완료! (Completed)")
    print("=" * 80)
    print(f"Updated GeoJSON saved to: {OUTPUT_PATH}")
    print()
    print("작업 내용:")
    print("  1. 경기도/강원도 개미굴 메우기 적용 완료")
    print("  2. 강원도 북부를 gangwon_boundaries와 합집합 완료")
    print()
    print("다음 단계:")
    print("  - QGIS 또는 geojson.io에서 결과 확인")
    print("  - 만족스러우면 원본 파일을 updated 파일로 교체")


if __name__ == "__main__":
    main()
