# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

import json
from config import BASE_PATH

# REGION_OPTION = ["경기도", "강원도"]
REGION_OPTION = None

# 파일 경로
input_file = os.path.join(BASE_PATH, "using_data","boundaries_KR_20220407_modified.geojson")
output_file = os.path.join(BASE_PATH, "static","whole.geojson")


print(f"\n파일 로딩 중: {input_file}")
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# admin_level 4인 지역만 필터링
level4_features = [f for f in data['features'] if f['properties'].get('admin_level') == 4]
print(f"admin_level 4 지역 수: {len(level4_features)}")

# whole.geojson 생성 (admin_level 4 polygon + 중심점 point)
all_features = []

# 1. Polygon/MultiPolygon features 추가
if REGION_OPTION:
    for feature in level4_features:
        props = feature['properties']
        if props.get('name', '') in ("강원도", "경기도"):
            all_features.append(feature)
else:
    all_features.extend(level4_features)

# 2. 중심점 Point features 추가
print("\n중심점 Point feature 생성 중...")
for feature in level4_features:
    props = feature['properties']
    name = props.get('name', '')
    name_en = props.get('name_en', '')
    center_lon = props.get('center_lon')
    center_lat = props.get('center_lat')

    

    if center_lon is not None and center_lat is not None:
        # Point feature 생성
        point_feature = {
            "type": "Feature",
            "properties": {
                "name": name,
                "name_en": name_en,
                "type": "center_point",
                "admin_level": 4
            },
            "geometry": {
                "type": "Point",
                "coordinates": [center_lon, center_lat]
            }
        }
        all_features.append(point_feature)
        print(f"  {name} ({name_en}) 중심점 추가: ({center_lon:.7f}, {center_lat:.7f})")

output_data = {
    "type": "FeatureCollection",
    "features": all_features
}

print(f"\n파일 저장 중: {output_file}")
print(f"  - Polygon features: {len(level4_features)}")
print(f"  - Point features: {len(all_features) - len(level4_features)}")
print(f"  - Total features: {len(all_features)}")

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("완료!")
print("=" * 80)
