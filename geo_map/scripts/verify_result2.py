# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import BASE_PATH
import geopandas as gpd

# 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 원본, 기존 업데이트, 새로운 업데이트 파일 비교
print("=" * 80)
print("File Comparison")
print("=" * 80)

# 1. 원본
print("\n[1] Original File")
gdf_original = gpd.read_file(os.path.join(BASE_PATH, 'using_data', 'boundaries_KR_20220407.geojson'))
print(f"  Total features: {len(gdf_original)}")
print(f"  Sample names: {gdf_original['name'].head(10).tolist()}")

# 경기도/강원도 찾기
gg_orig = gdf_original[gdf_original["name"].str.contains("경기", na=False)]
gw_orig = gdf_original[gdf_original["name"].str.contains("강원", na=False)]

print(f"  Gyeonggi count: {len(gg_orig)}")
if len(gg_orig) > 0:
    print(f"    Name: {gg_orig['name'].iloc[0]}")
    print(f"    Area: {gg_orig.geometry.iloc[0].area:.6f}")

print(f"  Gangwon count: {len(gw_orig)}")
if len(gw_orig) > 0:
    print(f"    Name: {gw_orig['name'].iloc[0]}")
    print(f"    Area: {gw_orig.geometry.iloc[0].area:.6f}")

# 2. 기존 업데이트 (잘못된 버전)
print("\n[2] Old Updated File (Wrong Version)")
gdf_old = gpd.read_file(os.path.join(BASE_PATH, 'using_data', 'boundaries_KR_20220407_updated.geojson'))
gg_old = gdf_old[gdf_old["name"].str.contains("경기", na=False)]
gw_old = gdf_old[gdf_old["name"].str.contains("강원", na=False)]

print(f"  Total features: {len(gdf_old)}")
print(f"  Gyeonggi count: {len(gg_old)}")
if len(gg_old) > 0:
    print(f"    Name: {gg_old['name'].iloc[0]}")
    print(f"    Area: {gg_old.geometry.iloc[0].area:.6f}")
else:
    print("    Status: NOT FOUND [X]")

print(f"  Gangwon count: {len(gw_old)}")
if len(gw_old) > 0:
    print(f"    Name: {gw_old['name'].iloc[0]}")
    print(f"    Area: {gw_old.geometry.iloc[0].area:.6f}")

# 3. 새로운 업데이트 (올바른 버전)
print("\n[3] New Updated V2 File (Correct Version)")
gdf_v2 = gpd.read_file(os.path.join(BASE_PATH, 'using_data', 'boundaries_KR_20220407_updated_v2.geojson'))
gg_v2 = gdf_v2[gdf_v2["name"].str.contains("경기", na=False)]
gw_v2 = gdf_v2[gdf_v2["name"].str.contains("강원", na=False)]

print(f"  Total features: {len(gdf_v2)}")
print(f"  Gyeonggi count: {len(gg_v2)}")
if len(gg_v2) > 0:
    print(f"    Name: {gg_v2['name'].iloc[0]}")
    print(f"    Area: {gg_v2.geometry.iloc[0].area:.6f}")
    print("    Status: FOUND [OK]")
else:
    print("    Status: NOT FOUND [X]")

print(f"  Gangwon count: {len(gw_v2)}")
if len(gw_v2) > 0:
    print(f"    Name: {gw_v2['name'].iloc[0]}")
    print(f"    Area: {gw_v2.geometry.iloc[0].area:.6f}")
    print("    Status: FOUND [OK]")

# 면적 변화 분석
print("\n" + "=" * 80)
print("Area Change Analysis")
print("=" * 80)

if len(gg_v2) > 0 and len(gg_orig) > 0:
    area_change_gg = gg_v2.geometry.iloc[0].area - gg_orig.geometry.iloc[0].area
    print(f"\nGyeonggi:")
    print(f"  Original area: {gg_orig.geometry.iloc[0].area:.6f}")
    print(f"  Updated area:  {gg_v2.geometry.iloc[0].area:.6f}")
    print(f"  Change: +{area_change_gg:.6f} (+{area_change_gg/gg_orig.geometry.iloc[0].area*100:.2f}%)")

if len(gw_v2) > 0 and len(gw_orig) > 0:
    area_change_gw = gw_v2.geometry.iloc[0].area - gw_orig.geometry.iloc[0].area
    print(f"\nGangwon:")
    print(f"  Original area: {gw_orig.geometry.iloc[0].area:.6f}")
    print(f"  Updated area:  {gw_v2.geometry.iloc[0].area:.6f}")
    print(f"  Change: +{area_change_gw:.6f} (+{area_change_gw/gw_orig.geometry.iloc[0].area*100:.2f}%)")

print("\n" + "=" * 80)
if len(gg_v2) > 0 and len(gw_v2) > 0:
    print("SUCCESS: Both Gyeonggi and Gangwon exist with updated northern borders!")
else:
    print("FAILED: Some provinces are missing")
print("=" * 80)
