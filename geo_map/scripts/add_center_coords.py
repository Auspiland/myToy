# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import os
from shapely.geometry import shape
from config import BASE_PATH

USING_DATA_PATH = os.path.join(BASE_PATH, "using_data")

# 처리할 파일들
TARGET_FILES = [
    "boundaries_KR_20220407.geojson",
    "new_prk_admbnda_adm2_wfp_20190624.geojson"
]

# 중심 좌표 참조 파일들
CENTER_FILES = [
    "kr_gis_osm_places_free_1.geojson",
    "kp_gis_osm_places_free_1.geojson"
]

def load_center_coordinates():
    """
    중심 좌표 파일에서 이름별 좌표 딕셔너리 생성.
    """
    center_dict = {}

    for filename in CENTER_FILES:
        filepath = os.path.join(USING_DATA_PATH, filename)
        print(f"중심 좌표 로딩 중: {filename}")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for feature in data.get('features', []):
            props = feature.get('properties', {})
            geom = feature.get('geometry', {})

            name = props.get('name')
            if name and geom.get('type') == 'Point':
                coords = geom.get('coordinates', [])
                if len(coords) >= 2:
                    # 중복된 이름이 있을 수 있으므로, 덮어쓰지 않고 유지
                    if name not in center_dict:
                        center_dict[name] = {
                            'lon': coords[0],
                            'lat': coords[1]
                        }

        print(f"  -> {len([k for k in center_dict])} 개의 이름 로딩됨")

    return center_dict

def add_center_to_geojson(filepath, center_dict):
    """
    GeoJSON 파일에 중심 좌표 추가.
    - 중심 좌표 파일에서 찾으면 그 값 사용
    - 없으면 geometry의 centroid 계산하여 사용
    """
    print(f"\n파일 처리 중: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    features = data.get('features', [])
    total = len(features)
    found_in_dict = 0
    calculated = 0
    already_has = 0

    for i, feature in enumerate(features):
        props = feature.get('properties', {})
        geom_dict = feature.get('geometry', {})

        # 이미 중심 좌표가 있는지 확인
        if 'center_lon' in props and 'center_lat' in props:
            already_has += 1
            continue

        # 행정구역 이름 찾기 (NAME_KEYS 순서로)
        NAME_KEYS = ("name", "NAME", "ADM2_KO", "ADM1_KO", "ADM0_KO")
        region_name = None
        for key in NAME_KEYS:
            if key in props and props[key]:
                region_name = str(props[key])
                break

        if not region_name:
            continue

        # 중심 좌표 찾기 또는 계산
        center_lon = None
        center_lat = None

        # 1. 중심 좌표 딕셔너리에서 찾기
        if region_name in center_dict:
            center_info = center_dict[region_name]
            center_lon = center_info['lon']
            center_lat = center_info['lat']
            found_in_dict += 1
        else:
            # 2. Geometry에서 centroid 계산
            try:
                geom = shape(geom_dict)
                if not geom.is_empty:
                    centroid = geom.centroid
                    center_lon = centroid.x
                    center_lat = centroid.y
                    calculated += 1
            except Exception as e:
                print(f"  경고: {region_name} - centroid 계산 실패: {e}")
                continue

        # properties에 추가
        if center_lon is not None and center_lat is not None:
            props['center_lon'] = center_lon
            props['center_lat'] = center_lat

        # 진행 상황 출력 (10%마다)
        if (i + 1) % max(1, total // 10) == 0:
            print(f"  진행: {i+1}/{total} ({(i+1)*100//total}%)")

    # 파일 저장
    print(f"  파일 저장 중...")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  완료!")
    print(f"    - 이미 중심좌표 있음: {already_has}")
    print(f"    - 참조파일에서 찾음: {found_in_dict}")
    print(f"    - 계산하여 추가: {calculated}")
    print(f"    - 전체: {total}")

def main():
    print("=" * 80)
    print("중심 좌표 추가 스크립트")
    print("=" * 80)

    # 1. 중심 좌표 로딩
    center_dict = load_center_coordinates()
    print(f"\n총 {len(center_dict)}개의 중심 좌표 로딩됨\n")

    # 2. 각 파일 처리
    for filename in TARGET_FILES:
        filepath = os.path.join(USING_DATA_PATH, filename)
        if os.path.exists(filepath):
            add_center_to_geojson(filepath, center_dict)
        else:
            print(f"\n경고: 파일을 찾을 수 없음 - {filepath}")

    print("\n" + "=" * 80)
    print("모든 작업 완료!")
    print("=" * 80)

if __name__ == "__main__":
    main()
