# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from shapely.geometry import Point, shape
from shapely.validation import make_valid
from shapely.prepared import prep
from shapely.ops import nearest_points
import json, os
import math

# 최소한의 이름 키만 사용 (ADM2_KO가 ADM1_KO보다 우선)
NAME_KEYS = ("name", "NAME", "ADM2_KO", "ADM1_KO", "ADM0_KO")

# 행정구역 레벨 순서 (상위 -> 하위)
ADMIN_LEVEL_ORDER = [
    "국",
    "도", "특별시", "광역시", "직할시", "특별자치시",
    "시", "군", "구", "구역",
    "읍", "면", "동",
    "리", "통", "노동자구", "지구",
    "반"
]

def _get_name(props: dict):
    for k in NAME_KEYS:
        v = props.get(k)
        if v:
            return str(v)
    return None

def _unpack_feature(feature_data):
    """feature_data 튜플 언패킹 (이전 버전 호환성)."""
    if len(feature_data) >= 5:
        return feature_data
    return feature_data[:4] + (None,)

def _get_admin_level(name: str):
    """
    행정구역 이름의 레벨을 반환. 낮을수록 상위 레벨.
    """
    for i, suffix in enumerate(ADMIN_LEVEL_ORDER):
        if name.endswith(suffix):
            return i
    return len(ADMIN_LEVEL_ORDER)  # 매칭되지 않으면 가장 마지막

def sort_by_admin_level(names):
    """
    행정구역 이름 리스트를 레벨 순서대로 정렬 (상위 -> 하위).
    """
    return sorted(names, key=_get_admin_level)

def load_features(paths):
    """
    여러 GeoJSON 파일에서 (geom, prepared_geom, name, all_names, center_coords) 리스트를 만든다.
    - all_names: NAME_KEYS에 해당하는 모든 값들의 리스트
    - center_coords: (center_lon, center_lat) 튜플 또는 None
    - 잘못되거나 빈 지오메트리는 제외
    """
    feats = []
    for p in paths:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)

        for feat in data.get("features", []):
            props = feat.get("properties", {}) or {}
            nm = _get_name(props)
            geom_dict = feat.get("geometry")
            if not nm or not geom_dict:
                continue

            # NAME_KEYS에 있는 모든 값을 추출
            all_names = []
            for k in NAME_KEYS:
                v = props.get(k)
                if v and str(v) not in all_names:
                    all_names.append(str(v))

            # 중심 좌표만 추출
            center_lon = props.get('center_lon')
            center_lat = props.get('center_lat')
            center_coords = (center_lon, center_lat) if center_lon is not None and center_lat is not None else None

            try:
                g = shape(geom_dict)
                if not g.is_valid:
                    g = make_valid(g)
                if g.is_empty:
                    continue
            except Exception:
                continue

            feats.append((g, prep(g), nm, all_names, center_coords))
    return feats

def query_names_at_lonlat(features, lon, lat, eps=1e-9):
    """
    포인트(lon, lat)를 포함(경계 포함)하는 모든 name을 반환.
    - 후보는 bbox로 1차 필터 → prepared covers/intersects로 최종 판정
    - 포함되는 행정구역이 없으면 가장 가까운 행정구역 기준 방향과 거리 정보를 반환
    """
    pt = Point(lon, lat)
    pt_buf = pt.buffer(eps)

    out = []
    for feature_data in features:
        g, pg, nm, all_names, center_coords = _unpack_feature(feature_data)

        minx, miny, maxx, maxy = g.bounds
        if not (minx <= lon <= maxx and miny <= lat <= maxy):
            continue
        if pg.covers(pt) or g.intersects(pt_buf):
            for name in all_names:
                if name not in out:
                    out.append(name)

    # 포함되는 행정구역이 없으면 가장 가까운 행정구역 정보 반환
    if not out:
        return find_nearest_region_info(features, lon, lat)

    # 행정구역 레벨 순서대로 정렬
    return sort_by_admin_level(list(set(out)))

def get_direction(lon1, lat1, lon2, lat2):
    """
    두 좌표 간의 방향을 8방향(북, 북동, 동, 남동, 남, 남서, 서, 북서)으로 반환.
    """
    dx = lon2 - lon1
    dy = lat2 - lat1

    angle = math.degrees(math.atan2(dy, dx))

    # atan2는 -180~180도 반환, 0도는 동쪽
    # 북쪽을 0도로 하기 위해 조정
    angle = (90 - angle) % 360

    if 337.5 <= angle or angle < 22.5:
        return "북"
    elif 22.5 <= angle < 67.5:
        return "북동"
    elif 67.5 <= angle < 112.5:
        return "동"
    elif 112.5 <= angle < 157.5:
        return "남동"
    elif 157.5 <= angle < 202.5:
        return "남"
    elif 202.5 <= angle < 247.5:
        return "남서"
    elif 247.5 <= angle < 292.5:
        return "서"
    else:
        return "북서"

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

def find_nearest_region_info(features, lon, lat):
    """
    포인트에서 가장 가까운 구/군/구역 단위 행정구역을 찾아
    "상위구역 포함 행정구역명 기준 약 방향 거리m 떨어짐" 형식의 문자열 리스트를 반환.
    """
    pt = Point(lon, lat)
    min_distance = float('inf')
    nearest_region = None
    nearest_all_names = []
    nearest_point_on_boundary = None

    # 구/군/구역 단위만 필터링하여 가장 가까운 행정구역 찾기
    for feature_data in features:
        g, pg, nm, all_names, center_coords = _unpack_feature(feature_data)

        if not is_district_level(nm):
            continue

        # 포인트에서 행정구역 경계까지의 최단거리 찾기
        nearest_pt = nearest_points(pt, g)[1]

        # 실제 미터 단위로 거리 계산
        distance_m = calculate_distance_meters(
            lon, lat,
            nearest_pt.x, nearest_pt.y
        )

        if distance_m < min_distance:
            min_distance = distance_m
            nearest_region = nm
            nearest_all_names = all_names
            nearest_point_on_boundary = nearest_pt

    if nearest_region is None:
        return []

    # 가장 가까운 경계 지점의 상위 행정구역들을 모두 찾기
    boundary_lon = nearest_point_on_boundary.x
    boundary_lat = nearest_point_on_boundary.y

    # 재귀 호출 방지를 위해 직접 포함 행정구역 찾기
    pt_boundary = Point(boundary_lon, boundary_lat)
    pt_buf = pt_boundary.buffer(1e-9)

    parent_regions = []
    for feature_data in features:
        g, pg, nm, all_names, center_coords = _unpack_feature(feature_data)

        minx, miny, maxx, maxy = g.bounds
        if not (minx <= boundary_lon <= maxx and miny <= boundary_lat <= maxy):
            continue
        if pg.covers(pt_boundary) or g.intersects(pt_buf):
            parent_regions.append(nm)

    parent_regions = list(set(parent_regions))

    # 가장 가까운 행정구역의 all_names를 사용 (NAME_KEYS에 있는 모든 값 포함)
    # 단, parent_regions에 있는 값들과 중복되지 않도록 함
    combined_names = []
    for name in nearest_all_names:
        if name not in combined_names:
            combined_names.append(name)
    for name in parent_regions:
        if name not in combined_names and name not in nearest_all_names:
            combined_names.append(name)

    # 행정구역 레벨 순서대로 정렬
    combined_names = sort_by_admin_level(combined_names)

    # 상위 구역들을 공백으로 연결
    full_region_name = ' '.join(combined_names) if combined_names else nearest_region

    # 방향 계산
    direction = get_direction(
        nearest_point_on_boundary.x,
        nearest_point_on_boundary.y,
        lon,
        lat
    )

    # 거리를 미터로 변환
    distance_m = calculate_distance_meters(
        nearest_point_on_boundary.x,
        nearest_point_on_boundary.y,
        lon,
        lat
    )

    result_str = f"{full_region_name} 기준 약 {direction}쪽 방향 {int(distance_m):,}m 떨어짐"
    return [result_str]

# ---------------- 사용 예 ----------------
if __name__ == "__main__":
    from config import BASE_PATH

    using_data_path = os.path.join(BASE_PATH, "using_data")
    files = (os.path.join(using_data_path, "boundaries_KR_20220407.geojson"),
             os.path.join(using_data_path, "new_prk_admbnda_adm2_wfp_20190624.geojson"))

    features = load_features(files)

    point = (116.4074, 39.9042)

    points = [
        # 대한민국 내부 (10)
        (126.9780, 37.5665),
        (126.7052, 37.4563),
        (129.0756, 35.1796),
        (128.6014, 35.8714),
        (126.8514, 35.1600),
        (127.3845, 36.3504),
        (129.3114, 35.5384),
        (126.5312, 33.4996),
        (128.8961, 37.7519),
        (129.3650, 36.0190),

        # 북한 내부 (5)
        (125.7625, 39.0392),
        (127.5364, 39.9185),
        (129.7740, 41.7956),
        (124.3980, 40.1000),
        (128.1790, 41.3970),

        # 한반도 외부 (5)
        (116.4074, 39.9042),
        (121.4737, 31.2304),
        (131.8855, 43.1155),
        (139.6917, 35.6895),
        (121.5654, 25.0330),
        (127.5000, 43.3000)
    ]

    for p in points:
        print(query_names_at_lonlat(features, *p))
