# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from shapely.geometry import Polygon, Point, mapping
from shapely.validation import make_valid
from shapely.geometry.polygon import orient
import os
import json
import math
import time, re
import webbrowser
import subprocess
from pathlib import Path
from typing import Optional


# point2region에서 필요한 함수들 import
from core.point2region import (
    load_features,
    sort_by_admin_level,
    find_nearest_region_info,
    query_names_at_lonlat,
    _unpack_feature,
    NAME_KEYS,
    ADMIN_LEVEL_ORDER
)
from src.common_utils import push_to_github

def sort_counterclockwise(points):
    if len(points) < 4:
        raise ValueError(f"입력 데이터는 4개이어야 합니다. 입력된 데이터 : {len(points)}개.")
    points = points[:4]
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    return sorted(points, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))

# 답변에 포함할 행정구역 레벨
ANSWER_LEVELS = ["국", "도", "특별시", "광역시", "직할시", "특별자치시", "시", "군", "구", "구역"]

def is_answer_level(name: str):
    """
    답변에 포함할 행정구역 레벨인지 확인.
    """
    return any(name.endswith(suffix) for suffix in ANSWER_LEVELS)

def is_provincial_level(name: str):
    """
    광역 단위(도, 특별시, 광역시, 직할시, 특별자치시)인지 확인.
    """
    provincial_suffixes = ["도", "특별시", "광역시", "직할시", "특별자치시"]
    return any(name.endswith(suffix) for suffix in provincial_suffixes)

def analyze_multipolygon_islands(geometry, rect_polygon, total_intersection):
    """
    멀티폴리곤에서 내륙과 섬을 구분하고, rect와의 겹침 비율을 계산.

    Args:
        geometry: 분석할 지역의 geometry (Polygon 또는 MultiPolygon)
        rect_polygon: 사각형 폴리곤
        total_intersection: 이미 계산된 rect_polygon.intersection(geometry)

    Returns:
        {
            "is_multipolygon": bool,
            "island_ratio_in_intersection": float,  # 드러난 부분(교차 영역) 중 섬이 차지하는 비율
            "is_island_dominant": bool,  # 섬이 주요 겹침 영역인지 여부 (40% 이상)
            "dominant_island_center": [lon, lat] or None  # 섬들의 중심 좌표 (근사값)
        }
    """
    if geometry.geom_type != 'MultiPolygon':
        return {
            "is_multipolygon": False,
            "island_ratio_in_intersection": 0,
            "is_island_dominant": False,
            "dominant_island_center": None
        }

    # 가장 큰 폴리곤을 내륙으로 간주
    mainland_polygon = max(geometry.geoms, key=lambda p: p.area)

    # 1. 내륙과 rect의 교차 면적 (A)
    mainland_intersection = rect_polygon.intersection(mainland_polygon)
    mainland_intersection_area = mainland_intersection.area if mainland_intersection else 0

    # 2. 전체 geometry와 rect의 교차 면적 (B) - 이미 계산된 값 사용
    total_intersection_area = total_intersection.area if total_intersection else 0

    # 3. 섬 교차 면적 = B - A
    islands_intersection_area = total_intersection_area - mainland_intersection_area

    # 4. 드러난 부분 중 섬이 차지하는 비율
    island_ratio_in_intersection = (
        islands_intersection_area / total_intersection_area
        if total_intersection_area > 0 else 0
    )

    # 5. 섬이 주요 겹침 영역인지 판단: 드러난 부분 중 40% 이상이 섬
    is_island_dominant = island_ratio_in_intersection >= 0.40

    # 6. 섬의 중심 좌표 (섬 영역들의 centroid로 근사)
    dominant_island_center = None
    if is_island_dominant and islands_intersection_area > 0:
        # 전체 교차 영역에서 내륙 교차 영역을 뺀 부분의 중심
        islands_intersection = total_intersection.difference(mainland_intersection) if mainland_intersection else total_intersection
        if islands_intersection and not islands_intersection.is_empty:
            centroid = islands_intersection.centroid
            dominant_island_center = [centroid.x, centroid.y]

    return {
        "is_multipolygon": True,
        "island_ratio_in_intersection": island_ratio_in_intersection,
        "is_island_dominant": is_island_dominant,
        "dominant_island_center": dominant_island_center
    }


def get_relative_direction(rect_center_lon, rect_center_lat, region_center_lon, region_center_lat):
    """
    사각형 중심에서 본 행정구역 중심의 방향을 9방향으로 반환.
    - 행정구역이 사각형 중심에 가까우면: "중심"
    - 그 외: "북부", "북동부", "동부", "남동부", "남부", "남서부", "서부", "북서부"
    """
    import math

    dx = region_center_lon - rect_center_lon
    dy = region_center_lat - rect_center_lat

    # 거리 계산
    distance = math.sqrt(dx**2 + dy**2)

    # 매우 가까우면 중심으로 간주
    if distance < 0.1:  # 약 11km 이내
        return "중심"

    # 8방향 판정 (균등 분할 45도)
    angle = math.degrees(math.atan2(dy, dx))
    angle = (90 - angle) % 360

    if 337.5 <= angle or angle < 22.5:
        return "북부"
    elif 22.5 <= angle < 67.5:
        return "북동부"
    elif 67.5 <= angle < 112.5:
        return "동부"
    elif 112.5 <= angle < 157.5:
        return "남동부"
    elif 157.5 <= angle < 202.5:
        return "남부"
    elif 202.5 <= angle < 247.5:
        return "남서부"
    elif 247.5 <= angle < 292.5:
        return "서부"
    else:
        return "북서부"

def get_region_representative_name(features, region_name, coverage_ratio, rect_center_lon, rect_center_lat, region_centers_cache, island_info=None, intersection=None):
    """
    광역 단위 지역의 포괄적 표현 생성.
    - 면적 95% 이상 포함: "서울특별시 전체"
    - 면적 70% 이상 포함: "서울특별시 대부분"
    - 섬이 주요 영역인 경우: "전라남도 북부 섬" 또는 "경상남도 남동부 섬"
    - 그 외: "서울특별시 [방향] 포함" (예: "강원도 북부 포함")
    """
    # 섬이 주요 영역인지 확인
    is_island_dominant = island_info and island_info.get("is_island_dominant", False)

    # 면적 기준 판정
    if coverage_ratio >= 0.95:
        return f"{region_name} 전체"
    elif coverage_ratio >= 0.70:
        return f"{region_name} 대부분"

    # 방향 기반 표현
    # 광역 단위의 중심 좌표 찾기 (캐시 활용)
    if region_name not in region_centers_cache:
        # 캐시에 없으면 features에서 찾기
        for feature_data in features:
            g, pg, nm, all_names, center_coords = _unpack_feature(feature_data)

            if region_name in all_names:
                if center_coords is not None:
                    region_centers_cache[region_name] = center_coords
                else:
                    centroid = g.centroid
                    region_centers_cache[region_name] = (centroid.x, centroid.y)
                break

    # 방향 계산: 행정구역 중심 -> 겹친 영역의 중심
    direction = None
    if region_name in region_centers_cache:
        region_center = region_centers_cache[region_name]

        # 겹친 영역의 중심 좌표 계산
        if is_island_dominant and island_info.get("dominant_island_center"):
            # 섬의 경우: 섬 교차 영역의 중심
            intersection_center_lon, intersection_center_lat = island_info["dominant_island_center"]
        elif intersection and not intersection.is_empty:
            # 일반적인 경우: 교차 영역의 중심
            intersection_centroid = intersection.centroid
            intersection_center_lon, intersection_center_lat = intersection_centroid.x, intersection_centroid.y
        else:
            # intersection이 없으면 rect 중심 사용 (폴백)
            intersection_center_lon, intersection_center_lat = rect_center_lon, rect_center_lat

        direction = get_relative_direction(
            region_center[0], region_center[1],           # 시작점: 행정구역 중심
            intersection_center_lon, intersection_center_lat  # 끝점: 겹친 영역의 중심
        )

    # 최종 표현 생성
    if direction:
        if is_island_dominant:
            # 섬이 주요 영역인 경우
            if direction == "중심":
                return f"{region_name} 섬"
            else:
                return f"{region_name} {direction} 섬"
        else:
            # 일반적인 경우
            if direction == "중심":
                return f"{region_name} 중심부 포함"
            else:
                return f"{region_name} {direction} 포함"

    # 중심을 찾지 못한 경우
    if is_island_dominant:
        return f"{region_name} 섬"
    return f"{region_name} 일부 포함"

def query_regions_in_rect(features, rect_coords, only_representive_text=False) -> dict:
    """
    사각형 영역에 포함되는 행정구역들을 반환.

    Returns:
    - {"representative": [...], "fully_contained": [...], "all_regions": [...],
       "provincial_regions": [...], "center": [lon, lat], "distance_info": None}
    """

    rect_polygon = Polygon(rect_coords)
    if not rect_polygon.is_valid:
        rect_polygon = make_valid(rect_polygon)

    centroid = rect_polygon.centroid
    center_lon, center_lat = centroid.x, centroid.y

    query_names_at_lonlat(features, center_lon, center_lat)

    fully_contained = []
    partially_contained = []
    provincial_regions = {}  # {region_name: {"coverage": ratio, "intersection": geometry}}
    region_centers_cache = {}
    island_info_cache = {}  # 섬 정보 캐시

    for feature_data in features:
        g, pg, nm, all_names, center_coords = _unpack_feature(feature_data)

        if not rect_polygon.intersects(g):
            continue

        valid_names = [name for name in all_names if is_answer_level(name)]
        if not valid_names:
            continue

        intersection = rect_polygon.intersection(g)
        coverage_ratio = (intersection.area / g.area) if g.area > 0 else 0
        is_full = coverage_ratio > 0.99

        for name in valid_names:
            if is_provincial_level(name):
                # 기존 coverage_ratio와 비교하여 더 큰 값으로 업데이트
                if name not in provincial_regions or coverage_ratio > provincial_regions[name]["coverage"]:
                    provincial_regions[name] = {
                        "coverage": coverage_ratio,
                        "intersection": intersection
                    }

                # 멀티폴리곤인 경우 섬 정보 분석 (광역 단위만)
                if name not in island_info_cache:
                    # 이미 계산된 intersection을 전달하여 중복 계산 방지
                    island_info = analyze_multipolygon_islands(g, rect_polygon, intersection)
                    island_info_cache[name] = island_info

            if is_full:
                if name not in fully_contained:
                    fully_contained.append(name)
            else:
                if name not in partially_contained:
                    partially_contained.append(name)

    representative = [
        get_region_representative_name(
            features, region_name, region_data["coverage"],
            center_lon, center_lat, region_centers_cache,
            island_info=island_info_cache.get(region_name),
            intersection=region_data["intersection"]
        )
        for region_name, region_data in provincial_regions.items()
    ]

    fully_contained = sort_by_admin_level(fully_contained)
    representative = sort_by_admin_level(representative)
    all_regions = sort_by_admin_level(list(set(fully_contained + partially_contained)))

    if not all_regions:
        distance_info = find_nearest_region_info(features, center_lon, center_lat)
        representative = distance_info if distance_info else []
    else:
        center_info = " ".join(query_names_at_lonlat(features, center_lon, center_lat)) + " 중심"
        representative.insert(0, center_info)

    if only_representive_text:
        return {"representative": ", ".join(representative)}

    provincial_names = list(provincial_regions.keys())

    return {
        "representative": representative,
        "fully_contained": fully_contained,
        # "partially_contained": partially_contained,
        "all_regions": all_regions,
        "provincial_regions": provincial_names,  # 시/도 단위 지역 이름 리스트
        "center": [center_lon, center_lat],
        "distance_info": None  # 이제 representative에 포함됨
    }


class Rect2Region():
    def __init__(self, files=None):
        if files == None:
            from config import BASE_PATH
            using_data_path = os.path.join(BASE_PATH, "using_data")
            files = (
                os.path.join(using_data_path, "boundaries_KR_20220407.geojson"),
                os.path.join(using_data_path, "new_prk_admbnda_adm2_wfp_20190624.geojson")
            )

        self.features = load_features(files)

        self.test_idx = 0
    
    def convert(self,rect_coords, only_representive_text = False):
        rect_coords = sort_counterclockwise(rect_coords)
        result = query_regions_in_rect(self.features, rect_coords, only_representive_text = only_representive_text)
        return result

    def convert_many(self,rect_coords_list, only_representive_text = False):
        result = []
        for rect in rect_coords_list:
            result.append(self.convert(rect, only_representive_text = only_representive_text))
        return result
    
    def show(self, result_initial):
        def _show(result):
            print("=" * 80)
            print(f"테스트 {self.test_idx}")
            print("=" * 80)

            # only_representive_text=True로 호출된 경우
            if 'representative' in result and len(result) == 1:
                print(f"대표 표현: {result['representative']}")
            else:
                # 전체 스키마가 반환된 경우
                print(f"중심 좌표: {result['center']}")
                print()
                print(f"광역 단위 대표 표현: {result['representative']}")
                print(f"완전히 포함된 지역: {result['fully_contained']}")
                print(f"전체 지역 (완전+일부): {result['all_regions']}")

            print()
            self.test_idx += 1

        if isinstance(result_initial, str):
            try:
                result_initial = json.loads(result_initial)
            except:
                raise ValueError("Rect2Region converter show ERROR : input result has invalid schema.")
        if isinstance(result_initial, dict):
            _show(result_initial)
        elif isinstance(result_initial, list):
            for result_one in result_initial:
                _show(result_one)


    def convert_json_file(self, input_file, output_file):
        """
        특정 스키마의 JSON 파일에서 region_text 필드를 변환.
        경고: hits.hits 스키마에 고정됨.
        """
        import json

        print("데이터를 읽는 중...")
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        total_hits = len(data['hits']['hits'])
        print(f"총 {total_hits}개의 항목을 처리합니다...")

        for idx, hit in enumerate(data['hits']['hits']):
            if (idx + 1) % 100 == 0:
                print(f"진행 중: {idx + 1}/{total_hits}")

            region_text = hit['_source'].get('region_text')
            if region_text:
                if isinstance(region_text, str):
                    region_coords = json.loads(region_text)
                else:
                    region_coords = region_text

                rect_coords = sort_counterclockwise(region_coords)
                result = self.convert(rect_coords)
                converted_text = ", ".join(result['representative'])
                hit['_source']['region_text'] = converted_text

        print("변환된 데이터를 저장하는 중...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"완료! 변환된 데이터가 {output_file}에 저장되었습니다.")


    def get_region_boundary(self, region_name):
        """
        행정구역의 경계 정보를 반환.

        Returns:
        - {"found": True, "name": str, "bounds": [min_lon, min_lat, max_lon, max_lat],
           "center": [lon, lat], "boundary_coords": [[lon, lat], ...]}
        - 찾지 못한 경우: {"found": False}
        """
        for feature_data in self.features:
            g, pg, nm, all_names, center_coords = _unpack_feature(feature_data)

            if region_name in all_names:
                minx, miny, maxx, maxy = g.bounds

                centroid = g.centroid
                # center_lon, center_lat = centroid.x, centroid.y  # 계산 중점
                center_lon, center_lat = center_coords

                boundary_coords = []
                if g.geom_type == 'Polygon':
                    boundary_coords = list(g.exterior.coords)
                elif g.geom_type == 'MultiPolygon':
                    largest_polygon = max(g.geoms, key=lambda p: p.area)
                    boundary_coords = list(largest_polygon.exterior.coords)

                boundary_coords = [[coord[0], coord[1]] for coord in boundary_coords]

                return {
                    "found": True,
                    "name": region_name,
                    "bounds": [minx, miny, maxx, maxy],
                    "center": [center_lon, center_lat],
                    "boundary_coords": boundary_coords
                }

        return {"found": False}

    def calculate_map_center_and_zoom(self, rect_coords, bounds_list=None):
        """지도 중심 좌표와 zoom 레벨 계산."""
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

    def create_geojson(self, rect_coords, output_path, result=None, openbrowser=False):
        """
        사각형 좌표로 GeoJSON 파일 생성 및 GitHub에 푸시.
        포함된 시/도 폴리곤과 중심점도 추가.
        """
        rect_coords = sort_counterclockwise(rect_coords)
        if result is None:
            result = self.convert(rect_coords)

        # Polygon 생성 후 orient로 반시계 방향 보장
        rect_polygon = Polygon(rect_coords)
        rect_polygon = orient(rect_polygon, sign=1.0)  # sign=1.0: counter-clockwise

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
            boundary_info = self.get_region_boundary(region_name)

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

        map_info = self.calculate_map_center_and_zoom(rect_coords, bounds_list)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)

        print(f"GeoJSON 파일이 저장되었습니다: {output_path}")
        print(f"포함된 시/도: {', '.join(provincial_regions)}")

        url = push_to_github(output_path)
        if not url:
            print("이 레포지토리는 비공개이거나 존재하지 않습니다. 지도 로딩을 중지합니다.")
            return geojson
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


# ---------------- 사용 예 ----------------
if __name__ == "__main__":
    converter = Rect2Region()

    # 테스트 케이스 1: 사용자 제공 좌표
    rect_coords = [
        [126.93167575079963, 37.10178611970895],
        [127.50557082786963, 37.10314793150034],
        [126.93507098285538, 36.64210788827871],
        [127.50553754496315, 36.643447265652945]
    ]
    rect_coords = sort_counterclockwise(rect_coords)

    result1 = converter.convert(rect_coords)
    converter.show(result1)

    # 테스트 케이스 2: 서울 전체를 포함하는 사각형
    rect_coords_seoul = [
        [126.7, 37.7],
        [127.3, 37.7],
        [126.7, 37.4],
        [127.3, 37.4]
    ]

    result2 = converter.convert(rect_coords_seoul)
    converter.show(result2)

    # 테스트 케이스 3: 바다 한가운데 (범위 밖)
    rect_coords_ocean = [
        [120.0, 35.0],
        [121.0, 35.0],
        [120.0, 34.0],
        [121.0, 34.0]
    ]

    result3 = converter.convert(rect_coords_ocean)
    converter.show(result3)


    print("=" * 80)

    result4 = converter.get_region_boundary("서울특별시")
    print(result4['name'])
    print(result4['bounds'])
    print(result4['center'])

    print("=" * 80)
    print("JSON 파일 변환 예제")
    print("=" * 80)

    # JSON 파일 변환 실행
    from config import BASE_PATH
    using_data_path = os.path.join(BASE_PATH, "using_data")
    input_file = os.path.join(using_data_path, "data.json")
    output_file = os.path.join(using_data_path, "converted_data.json")
    converter.convert_json_file(input_file, output_file)
