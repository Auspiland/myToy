# -*- coding: utf-8 -*-
"""
국경선(경기도 북부, 강원도 북부) 개미굴 메우기 스크립트

목표:
- 경기도/강원도 북부 경계선의 좁은 협곡(개미굴)만 메우기
- 바깥 테두리의 큰 굴곡은 유지
- 북위 37.5° 이상 지역만 자동 처리

방법:
1. 좌표계 변환 (WGS84 → EPSG:5179 미터 단위)
2. 경기도/강원도 추출
3. 북부 지역 (lat >= 37.5) 필터링
4. Closing 연산: buffer(+r) → buffer(-r)
5. 결과 저장 및 시각화
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import BASE_PATH
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, LineString, mapping
from shapely.ops import unary_union
from shapely.validation import make_valid
import json
import matplotlib.pyplot as plt
from pathlib import Path


# 설정
GEOJSON_PATH = os.path.join(BASE_PATH, "using_data", "boundaries_KR_20220407.geojson")
OUTPUT_DIR = os.path.join(BASE_PATH, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 파라미터
BUFFER_RADIUS = 100.0  # 미터 (개미굴 입구 폭의 절반, 약 200m 폭의 협곡을 메움)
TARGET_PROVINCES = ["경기도", "강원도", "강원특별자치도"]

# 사용자 제공 LineString - 이 선보다 북쪽만 처리
BORDER_LINE_COORDS = [
    [126.66456778654037, 37.7881205935217],
    [127.15549185560224, 38.2552398658961],
    [128.15832162525874, 38.25483819709771],
    [128.37347632819063, 38.482391795333626],
    [128.3616636225412, 38.6730793098983]
]

# 좌표계
CRS_WGS84 = "EPSG:4326"
CRS_METER = "EPSG:5179"  # 한국 중부원점 TM (미터 단위)


def load_and_filter_provinces(geojson_path, target_provinces):
    """
    GeoJSON 파일에서 특정 시/도만 추출.

    Args:
        geojson_path: GeoJSON 파일 경로
        target_provinces: 추출할 시/도 리스트 (예: ["경기도", "강원도"])

    Returns:
        GeoDataFrame (EPSG:4326)
    """
    print(f"[1/6] Loading GeoJSON: {geojson_path}")
    gdf = gpd.read_file(geojson_path)

    # name 필드 찾기 (일반적으로 'name', 'name_ko', 'ADM_NM' 등)
    name_fields = ['name', 'name_ko', 'NAME', 'ADM_NM', 'ADM1_KO', 'ADM1_NAME']
    name_col = None
    for field in name_fields:
        if field in gdf.columns:
            name_col = field
            break

    if name_col is None:
        raise ValueError(f"Name field not found. Available columns: {list(gdf.columns)}")

    print(f"Using name field: {name_col}")

    # 시/도 필터링
    mask = gdf[name_col].isin(target_provinces)
    filtered = gdf[mask].copy()

    if len(filtered) == 0:
        print(f"Warning: No provinces found. Available names:")
        print(gdf[name_col].unique())
        raise ValueError(f"No provinces found for: {target_provinces}")

    print(f"Found {len(filtered)} province(s): {filtered[name_col].tolist()}")
    return filtered


def extract_northern_boundary(gdf, border_line_coords):
    """
    사용자 제공 LineString보다 북쪽 경계선만 추출 (버퍼 회랑 방식).

    Args:
        gdf: GeoDataFrame (EPSG:4326)
        border_line_coords: LineString 좌표 리스트 [[lon, lat], ...]

    Returns:
        GeoDataFrame with northern parts only
    """
    print(f"[2/6] Extracting boundary above user-defined LineString")

    # LineString 생성
    border_line = LineString(border_line_coords)

    # LineString을 북쪽으로 연장하여 클리핑 폴리곤 생성
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]

    # LineString의 끝점을 bounds의 양 끝까지 확장
    extended_coords = [
        [bounds[0], border_line_coords[0][1]],  # 왼쪽 확장
        *border_line_coords,
        [bounds[2], border_line_coords[-1][1]]  # 오른쪽 확장
    ]

    # 북쪽 클리핑 폴리곤 생성 (LineString 위쪽 전체)
    clip_polygon_coords = [
        *extended_coords,
        [bounds[2], bounds[3]],  # 우상단
        [bounds[0], bounds[3]]   # 좌상단
    ]
    clip_polygon = Polygon(clip_polygon_coords)

    # Polygon validation
    if not clip_polygon.is_valid:
        clip_polygon = make_valid(clip_polygon)
        print("  Warning: clip_polygon was invalid, fixed with make_valid()")

    # 교차 영역만 추출
    gdf_clipped = gdf.copy()
    gdf_clipped['geometry'] = gdf_clipped['geometry'].apply(
        lambda geom: geom.intersection(clip_polygon) if geom.is_valid else make_valid(geom).intersection(clip_polygon)
    )

    # 빈 geometry 제거
    gdf_clipped = gdf_clipped[~gdf_clipped.geometry.is_empty]

    print(f"Clipped to region above border line: {len(gdf_clipped)} features")
    return gdf_clipped


def remove_holes(geometry):
    """
    Polygon/MultiPolygon의 내부 구멍(holes) 제거 - exterior만 유지.

    Args:
        geometry: Shapely Polygon/MultiPolygon

    Returns:
        Geometry without holes
    """
    if geometry.geom_type == 'Polygon':
        # Polygon의 exterior만 추출
        return Polygon(geometry.exterior.coords)
    elif geometry.geom_type == 'MultiPolygon':
        # 각 Polygon의 exterior만 추출
        polygons_without_holes = [Polygon(poly.exterior.coords) for poly in geometry.geoms]
        return MultiPolygon(polygons_without_holes)
    else:
        return geometry


def apply_closing_operation(geometry, buffer_radius):
    """
    형태학적 Closing 연산: buffer(+r) → buffer(-r) + 내부 구멍 제거

    Args:
        geometry: Shapely Polygon/MultiPolygon
        buffer_radius: 버퍼 반경 (미터)

    Returns:
        Closed geometry without holes
    """
    print(f"[3/6] Applying closing operation (radius={buffer_radius}m)")

    # Closing: 확장 후 수축
    expanded = geometry.buffer(buffer_radius)
    closed = expanded.buffer(-buffer_radius)

    # 내부 구멍 제거
    print(f"[3.5/6] Removing internal holes")
    closed_no_holes = remove_holes(closed)

    return closed_no_holes


def compute_added_area(original, closed):
    """
    Closing으로 추가된 면적 계산.

    Args:
        original: 원본 geometry
        closed: Closing 후 geometry

    Returns:
        added: 추가된 영역 (Polygon/MultiPolygon)
    """
    print(f"[4/6] Computing added area (filled ant tunnels)")

    added = closed.difference(original)

    # 면적 통계
    original_area_km2 = original.area / 1_000_000
    closed_area_km2 = closed.area / 1_000_000
    added_area_km2 = added.area / 1_000_000

    print(f"  Original area: {original_area_km2:.2f} km²")
    print(f"  Closed area: {closed_area_km2:.2f} km²")
    print(f"  Added area: {added_area_km2:.2f} km² (+{added_area_km2/original_area_km2*100:.2f}%)")

    return added


def create_result_geodataframe(original_gdf, closed_geometry, added_geometry, crs_meter):
    """
    결과 GeoDataFrame 생성 (원본, Closed, Added 레이어 포함).

    Args:
        original_gdf: 원본 GeoDataFrame
        closed_geometry: Closing 후 geometry
        added_geometry: 추가된 영역
        crs_meter: 미터 단위 CRS

    Returns:
        GeoDataFrame (3개 레이어)
    """
    print(f"[5/6] Creating result GeoDataFrame")

    # 원본 합치기
    original_union = unary_union(original_gdf.geometry)

    result = gpd.GeoDataFrame({
        'layer': ['original', 'closed', 'added'],
        'geometry': [original_union, closed_geometry, added_geometry]
    }, crs=crs_meter)

    return result


def visualize_results(gdf_wgs84, output_path):
    """
    결과 시각화 및 PNG 저장.

    Args:
        gdf_wgs84: GeoDataFrame (EPSG:4326)
        output_path: 저장 경로
    """
    print(f"[6/6] Visualizing results")

    fig, ax = plt.subplots(1, 1, figsize=(15, 10))

    # 레이어별 색상
    colors = {
        'original': 'black',
        'closed': 'red',
        'added': 'blue'
    }

    for idx, row in gdf_wgs84.iterrows():
        layer = row['layer']
        color = colors.get(layer, 'gray')
        alpha = 0.3 if layer == 'added' else 0.7

        if row.geometry.is_empty:
            continue

        gdf_wgs84[gdf_wgs84['layer'] == layer].plot(
            ax=ax,
            color=color,
            alpha=alpha,
            edgecolor=color,
            linewidth=2 if layer in ['original', 'closed'] else 0,
            label=f"{layer.capitalize()} ({colors[layer]})"
        )

    ax.set_title("Border Ant Tunnels Filling Result\n(Black: Original, Red: Closed, Blue: Added)", fontsize=14)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved visualization: {output_path}")
    plt.close()


def main():
    """메인 실행 함수"""

    print("=" * 80)
    print("국경선 개미굴 메우기 (Border Ant Tunnels Filling)")
    print("=" * 80)
    print(f"Target provinces: {TARGET_PROVINCES}")
    print(f"Buffer radius: {BUFFER_RADIUS}m (fills tunnels < {BUFFER_RADIUS*2}m width)")
    print(f"Border line points: {len(BORDER_LINE_COORDS)} points")
    print()

    # 1. GeoJSON 로드 및 필터링
    gdf_original = load_and_filter_provinces(GEOJSON_PATH, TARGET_PROVINCES)

    # 2. 북부 지역 추출 (사용자 제공 LineString 기준)
    gdf_north = extract_northern_boundary(gdf_original, BORDER_LINE_COORDS)

    # 3. 좌표계 변환 (WGS84 → 미터)
    print(f"Converting CRS: {CRS_WGS84} → {CRS_METER}")
    gdf_meter = gdf_north.to_crs(CRS_METER)

    # 4. Geometry 합치기
    original_union = unary_union(gdf_meter.geometry)

    # 5. Closing 연산
    closed_geometry = apply_closing_operation(original_union, BUFFER_RADIUS)

    # 6. 추가된 면적 계산
    added_geometry = compute_added_area(original_union, closed_geometry)

    # 7. 결과 GeoDataFrame 생성
    result_gdf = create_result_geodataframe(gdf_meter, closed_geometry, added_geometry, CRS_METER)

    # 8. WGS84로 복원
    result_gdf_wgs84 = result_gdf.to_crs(CRS_WGS84)

    # 9. 저장
    output_geojson = os.path.join(OUTPUT_DIR, "border_fixed_with_layers.geojson")
    result_gdf_wgs84.to_file(output_geojson, driver="GeoJSON")
    print(f"\nSaved result GeoJSON: {output_geojson}")

    # 10. Closed 결과만 별도 저장
    closed_only = result_gdf_wgs84[result_gdf_wgs84['layer'] == 'closed'].copy()
    output_closed = os.path.join(OUTPUT_DIR, "border_fixed_closed_only.geojson")
    closed_only.to_file(output_closed, driver="GeoJSON")
    print(f"Saved closed-only GeoJSON: {output_closed}")

    # 11. 시각화
    output_png = os.path.join(OUTPUT_DIR, "border_fixed_visualization.png")
    visualize_results(result_gdf_wgs84, output_png)

    print()
    print("=" * 80)
    print("완료! (Completed)")
    print("=" * 80)
    print(f"출력 파일:")
    print(f"  1. 레이어 포함: {output_geojson}")
    print(f"  2. Closed 결과만: {output_closed}")
    print(f"  3. 시각화: {output_png}")
    print()
    print("다음 단계:")
    print("  - QGIS 또는 geojson.io에서 결과 확인")
    print("  - 만족스러우면 원본 GeoJSON 파일 교체")
    print("  - BUFFER_RADIUS 조정 후 재실행 가능")


if __name__ == "__main__":
    main()
