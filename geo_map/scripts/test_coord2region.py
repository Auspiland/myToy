# -*- coding: utf-8 -*-
"""
coord2region.py 테스트 스크립트
"""
import sys
import os

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.coord2region import list_regions_in_center_box, get_representative_region, NAME_COL

if __name__ == "__main__":
    rect_coords = [
        [126.93167575079963, 37.10178611970895],
        [127.50557082786963, 37.10314793150034],
        [126.93507098285538, 36.64210788827871],
        [127.50553754496315, 36.643447265652945]
    ]

    # 1) 중앙 박스 내 도시/군/구 목록 (ratio 방식만)
    print("=" * 80)
    print("테스트 1: 중앙 박스 내 지역 목록")
    print("=" * 80)
    gdf_center = list_regions_in_center_box(
        rect_coords,
        center_ratio=0.70  # 가운데 70%
    )
    print(f"\n[중앙 박스 포함 지역 수] {len(gdf_center)}")
    if len(gdf_center):
        # 이름 + 상위지역 간단 출력
        cols = [NAME_COL, "fclass", "type", "country", "level", "parent_sgg", "parent_sido", "match_source"]
        print(gdf_center[cols].head(30).to_string(index=False))

    # 2) 대표 지역명 하나 (상위지역 포함)
    print("\n" + "=" * 80)
    print("테스트 2: 대표 지역명")
    print("=" * 80)
    result = get_representative_region(rect_coords)
    print("대표 지역명:", result)
