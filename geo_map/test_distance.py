# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from shapely.geometry import Point, shape
from shapely.ops import nearest_points
import json
import os
import math

def calculate_distance_meters(lon1, lat1, lon2, lat2):
    """
    두 좌표 간의 거리를 미터 단위로 계산 (Haversine formula).
    """
    R = 6371000  # 지구 반경 (미터)

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def is_district_level(name):
    """
    행정구역 이름이 구/군/구역 단위인지 확인.
    """
    district_suffixes = ('구', '군', '구역')
    return any(name.endswith(suffix) for suffix in district_suffixes)

BASE_PATH = r"C:\Users\T3Q\jeonghan\Eunhyea_Assist\geo_map"

# 파일 로드
files = [
    os.path.join(BASE_PATH,"ns_korea_shp","boundaries_KR_20220407.geojson"),
    os.path.join(BASE_PATH,"prk_adm_wfp_20190624_shp","new_prk_admbnda_adm2_wfp_20190624.geojson")
]

features = []
kr_count = 0
prk_count = 0

for file_path in files:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    is_prk = "prk" in file_path.lower()

    for feat in data.get("features", []):
        props = feat.get("properties", {}) or {}
        name_keys = ("name", "NAME", "ADM2_KO", "ADM1_KO")
        nm = None
        for k in name_keys:
            v = props.get(k)
            if v:
                nm = str(v)
                break

        if nm and is_district_level(nm):
            geom = shape(feat.get("geometry"))
            features.append((geom, nm))
            if is_prk:
                prk_count += 1
            else:
                kr_count += 1

print(f"대한민국 구/군/구역: {kr_count}개")
print(f"북한 구/군/구역: {prk_count}개")

# 테스트 좌표
test_lon, test_lat = 127.5000, 43.3000
pt = Point(test_lon, test_lat)

print(f"테스트 좌표: ({test_lon}, {test_lat})")
print(f"총 구/군/구역 개수: {len(features)}\n")

# 가장 가까운 5개 찾기
distances = []
for g, nm in features:
    nearest_pt = nearest_points(pt, g)[1]
    distance_m = calculate_distance_meters(
        test_lon, test_lat,
        nearest_pt.x, nearest_pt.y
    )
    distances.append((distance_m, nm, nearest_pt.x, nearest_pt.y))

distances.sort()

print("가장 가까운 5개 행정구역:")
for i, (dist, name, lon, lat) in enumerate(distances[:5]):
    print(f"{i+1}. {name}: {dist/1000:.2f}km (경계점: {lon:.4f}, {lat:.4f})")
