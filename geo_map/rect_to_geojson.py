# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import os
import math
from rect2region import Rect2Region

def calculate_map_center_and_zoom(rect_coords, bounds_list=None):
    """
    rect_coords의 중심 좌표와 적절한 zoom 레벨을 계산합니다.

    Parameters:
    - rect_coords: [[lon1, lat1], [lon2, lat2], [lon3, lat3], [lon4, lat4]] 형태의 사각형 좌표
    - bounds_list: 도 폴리곤의 bounds 리스트 [[min_lon, min_lat, max_lon, max_lat], ...]

    Returns:
    - dict: {'center': [lon, lat], 'zoom': zoom_level}
        - center: 소수점 6자리까지 반올림된 중심 좌표 (rect_coords 기준)
        - zoom: 계산된 zoom 레벨 (bounds_list 포함)
    """
    # 중심 좌표는 rect_coords 기준으로 계산
    rect_lons = [coord[0] for coord in rect_coords]
    rect_lats = [coord[1] for coord in rect_coords]

    center_lon = round((max(rect_lons) + min(rect_lons)) / 2, 6)
    center_lat = round((max(rect_lats) + min(rect_lats)) / 2, 6)

    # 범위 계산 시작값
    min_lon = min(rect_lons)
    max_lon = max(rect_lons)
    min_lat = min(rect_lats)
    max_lat = max(rect_lats)

    # bounds_list가 있으면 범위 확장
    if bounds_list:
        for bounds in bounds_list:
            # bounds = [min_lon, min_lat, max_lon, max_lat]
            min_lon = min(min_lon, bounds[0])
            min_lat = min(min_lat, bounds[1])
            max_lon = max(max_lon, bounds[2])
            max_lat = max(max_lat, bounds[3])

    lon_range = max_lon - min_lon
    lat_range = max_lat - min_lat

    # zoom 레벨 계산
    # zoom 10일 때: 가로(경도) 0.8, 세로(위도) 0.5
    k_lon = 0.8 * (2 ** 10)
    k_lat = 0.6 * (2 ** 10)

    zoom_lon = -math.log2(lon_range / k_lon) if lon_range > 0 else 10.0
    zoom_lat = -math.log2(lat_range / k_lat) if lat_range > 0 else 10.0

    zoom = round(min(zoom_lon, zoom_lat), 1)

    return {
        'center': [center_lon, center_lat],
        'zoom': zoom
    }

def create_geojson_from_rect(rect_coords, output_path):
    """
    사각형 좌표를 입력받아 GeoJSON 파일을 생성합니다.

    GeoJSON에 포함될 정보:
    1) 입력한 rect_coord 도형
    2) 일부 혹은 전체가 포함된 시/도 단위 지역의 폴리곤 좌표 데이터
    3) 2번에서 추가한 시/도 단위 지역의 중심 좌표점

    Parameters:
    - rect_coords: [[lon1, lat1], [lon2, lat2], [lon3, lat3], [lon4, lat4]] 형태의 사각형 좌표
    - output_path: 저장할 GeoJSON 파일 경로

    Returns:
    - dict: {'geojson': GeoJSON 데이터, 'map_info': {'center': [lon, lat], 'zoom': zoom_level}}
    """
    # Rect2Region 인스턴스 생성
    converter = Rect2Region()

    # 사각형 영역에 포함되는 행정구역 정보 조회
    result = converter.convert(rect_coords)

    # GeoJSON 구조 초기화
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # 1) 입력한 rect_coord 도형 추가
    rect_feature = {
        "type": "Feature",
        "properties": {
            "type": "input_rectangle",
            "center": result['center']
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [rect_coords + [rect_coords[0]]]  # 닫힌 폴리곤을 위해 첫 좌표를 마지막에 추가
        }
    }
    geojson["features"].append(rect_feature)

    # 2, 3) 시/도 단위 지역의 폴리곤 좌표와 중심 좌표 추가
    provincial_regions = result.get('provincial_regions', [])
    bounds_list = []  # zoom 계산용 bounds만 수집

    for region_name in provincial_regions:
        # get_region_boundary로 해당 시/도의 경계 및 중심 좌표 가져오기
        boundary_info = converter.get_region_boundary(region_name)

        if boundary_info.get('found'):
            # bounds 수집 (zoom 계산용)
            bounds_list.append(boundary_info['bounds'])

            # 2) 시/도 단위 지역의 폴리곤 추가
            polygon_feature = {
                "type": "Feature",
                "properties": {
                    "name": region_name,
                    "type": "provincial_region"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [boundary_info['boundary_coords']]
                }
            }
            geojson["features"].append(polygon_feature)

            # 3) 시/도 단위 지역의 중심 좌표점 추가
            center_feature = {
                "type": "Feature",
                "properties": {
                    "name": region_name,
                    "type": "provincial_center"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": boundary_info['center']
                }
            }
            geojson["features"].append(center_feature)

    # 모든 폴리곤의 bounds를 포함하여 지도 중심과 zoom 레벨 계산
    map_info = calculate_map_center_and_zoom(rect_coords, bounds_list)

    # GeoJSON 파일 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"GeoJSON 파일이 저장되었습니다: {output_path}")
    print(f"포함된 시/도: {', '.join(provincial_regions)}")
    print(f"\n지도 설정 정보:")
    print(f"  - 중심 좌표: {map_info['center']}")
    print(f"  - Zoom 레벨: {map_info['zoom']}")

    url = push_github(output_path)
    print(url)
    repo = url.replace("https://github.com/", "")
    repo = repo.replace("/tree/", "/blob/")

    import time
    import webbrowser
    time.sleep(1)
    link = f"https://geojson.io/#id=github:{repo}"+f"&map={"/".join(list(map(str,[map_info['zoom'],map_info['center'][1],map_info['center'][0]])))}"
    print("You can view the map at the following URL:")
    print(link)

    webbrowser.open(link)

    return geojson

def push_github(file_path):
    import subprocess
    from pathlib import Path

    file_path = Path(file_path)
    repo_dir = Path(r"C:\Users\T3Q\jeonghan\my_github\myToy")
    github_url = r"https://github.com/Auspiland/myToy.git"  # 직접 URL
    rel_file_path = file_path.relative_to(repo_dir)

    commit_msg = f"{Path(rel_file_path).name} 파일 자동 추가"

    subprocess.run(["git", "add", rel_file_path], cwd=repo_dir)
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_dir)
    subprocess.run(["git", "push", github_url, "main"], cwd=repo_dir)
    print("파일 업로드 완료!!")
    
    return r"https://github.com/Auspiland/myToy/tree/main/geo_map/static/"+ Path(rel_file_path).name



# ---------------- 사용 예 ----------------
if __name__ == "__main__":
    # 테스트 케이스 1: 사용자 제공 좌표
    rect_coords = [
        [126.93167575079963, 37.10178611970895],
        [127.50557082786963, 37.10314793150034],
        [127.50553754496315, 36.643447265652945],
        [126.93507098285538, 36.64210788827871]
    ]

    # static 폴더에 저장
    output_path = r"C:\Users\T3Q\jeonghan\my_github\myToy\geo_map\static\test_rect.geojson"

    # GeoJSON 생성 및 저장
    geojson_data = create_geojson_from_rect(rect_coords, output_path)

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
