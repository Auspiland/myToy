# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
from shapely.geometry import shape

# 파일 경로
input_file = r'C:\Users\T3Q\jeonghan\my_github\myToy\geo_map\using_data\boundaries_KR_20220407_updated.geojson'
output_file = r'C:\Users\T3Q\jeonghan\my_github\myToy\geo_map\not_using_data\whole.geojson'

# 인천광역시 하드코딩 좌표
INCHEON_HARDCODED = {
    'lon': 126.6176012,
    'lat': 37.4792081
}

print("=" * 80)
print("중심 좌표 계산 및 업데이트")
print("=" * 80)

print(f"\n파일 로딩 중: {input_file}")
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# admin_level 4인 지역만 필터링
level4_features = [f for f in data['features'] if f['properties'].get('admin_level') == 4]
print(f"admin_level 4 지역 수: {len(level4_features)}")

print("\n중심 좌표 계산 중...")
print("-" * 80)

for feature in level4_features:
    props = feature['properties']
    geom_dict = feature['geometry']

    name = props.get('name', '')
    name_en = props.get('name_en', '')

    # Geometry에서 centroid 계산
    try:
        geom = shape(geom_dict)
        if not geom.is_empty:
            centroid = geom.centroid
            calculated_lon = centroid.x
            calculated_lat = centroid.y

            # 인천광역시 특별 처리
            if name_en == 'Incheon':
                print(f"\n{name} ({name_en}):")
                print(f"  계산된 중심점: ({calculated_lon:.10f}, {calculated_lat:.10f})")
                print(f"  하드코딩 중심점: ({INCHEON_HARDCODED['lon']:.10f}, {INCHEON_HARDCODED['lat']:.10f})")
                print(f"  차이: lon={abs(calculated_lon - INCHEON_HARDCODED['lon']):.10f}, lat={abs(calculated_lat - INCHEON_HARDCODED['lat']):.10f}")
                print(f"  [INFO] 하드코딩 값 사용")

                # 하드코딩 값 사용
                props['center_lon'] = INCHEON_HARDCODED['lon']
                props['center_lat'] = INCHEON_HARDCODED['lat']
            else:
                # 계산된 값 사용
                props['center_lon'] = calculated_lon
                props['center_lat'] = calculated_lat
                print(f"{name} ({name_en}): ({calculated_lon:.6f}, {calculated_lat:.6f})")

    except Exception as e:
        print(f"[ERROR] {name} ({name_en}) - centroid 계산 실패: {e}")

print("\n" + "-" * 80)
print(f"중심 좌표 계산 완료: {len(level4_features)}개 지역")

# 원본 데이터에 중심점 좌표를 추가하여 업데이트된 파일 저장
updated_input_file_path = input_file.replace('.geojson', '_updated.geojson')
print(f"\n업데이트된 원본 파일 저장 중: {updated_input_file_path}")
with open(updated_input_file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("저장 완료.")

# whole.geojson 생성 (admin_level 4 polygon + 중심점 point)
all_features = []

# 1. Polygon/MultiPolygon features 추가
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
