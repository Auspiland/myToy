# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import math
import time
import webbrowser
import subprocess
from pathlib import Path
from shapely.geometry import Polygon, mapping
from shapely.geometry.polygon import orient
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

    # Polygon 생성 후 orient로 반시계 방향 보장
    rect_polygon = Polygon(rect_coords)
    rect_polygon = orient(rect_polygon, sign=1.0)

    geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"type": "input_rectangle", "center": result['center']},
            "geometry": mapping(rect_polygon)
        }]
    }

    provincial_regions = result.get('provincial_regions', [])
    bounds_list = []

    for region_name in provincial_regions:
        boundary_info = converter.get_region_boundary(region_name)

        if boundary_info.get('found'):
            bounds_list.append(boundary_info['bounds'])

            # Polygon 생성 후 orient로 반시계 방향 보장
            boundary_polygon = Polygon(boundary_info['boundary_coords'])
            boundary_polygon = orient(boundary_polygon, sign=1.0)

            geojson["features"].append({
                "type": "Feature",
                "properties": {"name": region_name, "type": "provincial_region"},
                "geometry": mapping(boundary_polygon)
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
    import os
    file_path = Path(file_path)
    repo_dir = Path(BASE_PATH).parent  # myToy 디렉토리
    rel_file_path = file_path.relative_to(repo_dir)

    # origin remote 확인
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=str(repo_dir),
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Git remote 'origin'이 설정되어 있지 않습니다.\n"
            f"Repository: {repo_dir}\n"
            f"다음 명령어로 origin을 추가하세요:\n"
            f"git remote add origin <repository-url>"
        )

    commit_msg = f"{file_path.name} 파일 자동 추가"

    # git add
    add_result = subprocess.run(
        ["git", "add", str(rel_file_path)],
        cwd=str(repo_dir),
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    if add_result.returncode != 0:
        raise RuntimeError(f"git add 실패:\n{add_result.stderr}")

    # git commit
    commit_result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        cwd=str(repo_dir),
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    # commit이 실패해도 괜찮음 (변경사항이 없을 수 있음)

    # git push
    push_result = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=str(repo_dir),
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    if push_result.returncode != 0:
        raise RuntimeError(
            f"git push 실패:\n{push_result.stderr}\n\n"
            f"가능한 원인:\n"
            f"1. 인증 문제 - GitHub 토큰/SSH 키 확인\n"
            f"2. 권한 문제 - repository 쓰기 권한 확인\n"
            f"3. 브랜치 문제 - main 브랜치 존재 확인"
        )

    print("파일 업로드 완료!!")
    return f"https://github.com/Auspiland/myToy/tree/main/{str(rel_file_path).replace(os.sep, '/')}"

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
