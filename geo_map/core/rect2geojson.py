# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import math
import time
import webbrowser
import subprocess
from pathlib import Path
from core.rect2region import Rect2Region

def calculate_map_center_and_zoom(rect_coords, bounds_list=None):
    """
    지도 중심 좌표와 zoom 레벨 계산.

    Returns:
    - {'center': [lon, lat], 'zoom': zoom_level}
    """
    rect_lons = [coord[0] for coord in rect_coords]
    rect_lats = [coord[1] for coord in rect_coords]

    center_lon = round((max(rect_lons) + min(rect_lons)) / 2, 6)
    center_lat = round((max(rect_lats) + min(rect_lats)) / 2, 6)

    min_lon, max_lon = min(rect_lons), max(rect_lons)
    min_lat, max_lat = min(rect_lats), max(rect_lats)

    if bounds_list:
        for bounds in bounds_list:
            min_lon = min(min_lon, bounds[0])
            min_lat = min(min_lat, bounds[1])
            max_lon = max(max_lon, bounds[2])
            max_lat = max(max_lat, bounds[3])

    lon_range = max_lon - min_lon
    lat_range = max_lat - min_lat

    k_lon = 0.8 * (2 ** 10)
    k_lat = 0.6 * (2 ** 10)

    zoom_lon = -math.log2(lon_range / k_lon) if lon_range > 0 else 10.0
    zoom_lat = -math.log2(lat_range / k_lat) if lat_range > 0 else 10.0

    return {
        'center': [center_lon, center_lat],
        'zoom': round(min(zoom_lon, zoom_lat), 1)
    }

def create_geojson_from_rect(rect_coords, output_path, openbrowser=False):
    """
    사각형 좌표로 GeoJSON 파일 생성 및 GitHub에 푸시.
    포함된 시/도 폴리곤과 중심점도 추가.
    """
    converter = Rect2Region()
    result = converter.convert(rect_coords)

    geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"type": "input_rectangle", "center": result['center']},
            "geometry": {"type": "Polygon", "coordinates": [rect_coords + [rect_coords[0]]]}
        }]
    }

    provincial_regions = result.get('provincial_regions', [])
    bounds_list = []

    for region_name in provincial_regions:
        boundary_info = converter.get_region_boundary(region_name)

        if boundary_info.get('found'):
            bounds_list.append(boundary_info['bounds'])

            geojson["features"].append({
                "type": "Feature",
                "properties": {"name": region_name, "type": "provincial_region"},
                "geometry": {"type": "Polygon", "coordinates": [boundary_info['boundary_coords']]}
            })

            geojson["features"].append({
                "type": "Feature",
                "properties": {"name": region_name, "type": "provincial_center"},
                "geometry": {"type": "Point", "coordinates": boundary_info['center']}
            })

    map_info = calculate_map_center_and_zoom(rect_coords, bounds_list)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"GeoJSON 파일이 저장되었습니다: {output_path}")
    print(f"포함된 시/도: {', '.join(provincial_regions)}")
    print(f"\n지도 설정 정보:")
    print(f"  - 중심 좌표: {map_info['center']}")
    print(f"  - Zoom 레벨: {map_info['zoom']}")

    url = push_github(output_path)
    print(url)

    repo = url.replace("https://github.com/", "").replace("/tree/", "/blob/")
    zoom, lat, lon = map_info['zoom'], map_info['center'][1], map_info['center'][0]
    link = f"https://geojson.io/#id=github:{repo}&map={zoom}/{lat}/{lon}"

    print("You can view the map at the following URL:")
    print(link)

    if openbrowser:
        time.sleep(1)
        webbrowser.open(link)

    return geojson

def push_github(file_path):
    from config import BASE_PATH
    file_path = Path(file_path)
    repo_dir = Path(BASE_PATH).parent.parent
    github_url = r"https://github.com/Auspiland/myToy.git"
    rel_file_path = file_path.relative_to(repo_dir)

    commit_msg = f"{rel_file_path.name} 파일 자동 추가"

    subprocess.run(["git", "add", rel_file_path], cwd=repo_dir)
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_dir)
    subprocess.run(["git", "push", github_url, "main"], cwd=repo_dir)
    print("파일 업로드 완료!!")

    return f"https://github.com/Auspiland/myToy/tree/main/geo_map/static/{rel_file_path.name}"

def run_main(rect_coords, data_name, print_info=False, openbrowser = False):
    from config import BASE_PATH
    import os
    output_path = os.path.join(BASE_PATH, "static", f"{data_name}.geojson")
    geojson_data = create_geojson_from_rect(rect_coords, output_path, openbrowser=openbrowser)

    if print_info:
        print("\n생성된 GeoJSON 구조:")
        print(f"- 총 features 수: {len(geojson_data['features'])}")
        for feature in geojson_data['features']:
            props = feature['properties']
            geom_type = feature['geometry']['type']
            if props['type'] == 'input_rectangle':
                print(f"  - 입력 사각형 ({geom_type})")
            elif props['type'] == 'provincial_region':
                print(f"  - {props['name']} 폴리곤 ({geom_type})")
            elif props['type'] == 'provincial_center':
                print(f"  - {props['name']} 중심점 ({geom_type})")

# ---------------- 사용 예 ----------------
if __name__ == "__main__":
    # 테스트 케이스 1: 사용자 제공 좌표
    rect_coords = [
        [126.93167575079963, 37.10178611970895],
        [127.50557082786963, 37.10314793150034],
        [127.50553754496315, 36.643447265652945],
        [126.93507098285538, 36.64210788827871]
    ]

    run_main(rect_coords, "test_rect", print_info=True)
