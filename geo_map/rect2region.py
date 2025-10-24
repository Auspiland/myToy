# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from shapely.geometry import Polygon, Point
from shapely.validation import make_valid
import os

# point2region에서 필요한 함수들 import
from point2region import (
    load_features,
    sort_by_admin_level,
    find_nearest_region_info,
    get_direction,
    NAME_KEYS,
    ADMIN_LEVEL_ORDER
)

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

    # 8방향 판정
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

def get_region_representative_name(features, region_name, coverage_ratio, rect_center_lon, rect_center_lat, region_centers_cache):
    """
    광역 단위 지역의 포괄적 표현 생성.
    - 면적 95% 이상 포함: "서울특별시 전체"
    - 면적 70% 이상 포함: "서울특별시 대부분"
    - 그 외: "서울특별시 [방향] 포함" (예: "강원도 북부 포함")
    """
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
            # feature_data는 (g, pg, nm, all_names, center_coords) 튜플
            if len(feature_data) >= 5:
                g, pg, nm, all_names, center_coords = feature_data
            else:
                # 이전 버전 호환성
                g, pg, nm, all_names = feature_data[:4]
                center_coords = None

            if region_name in all_names:
                # center_coords에서 중심 좌표 읽기
                if center_coords is not None:
                    region_centers_cache[region_name] = center_coords
                else:
                    # 없으면 centroid 계산
                    centroid = g.centroid
                    region_centers_cache[region_name] = (centroid.x, centroid.y)
                break

    # 캐시에서 중심 좌표 가져오기
    if region_name in region_centers_cache:
        region_center = region_centers_cache[region_name]
        # 방향 수정: 행정구역 중심 -> 사각형 중심 방향
        direction = get_relative_direction(
            region_center[0], region_center[1],
            rect_center_lon, rect_center_lat
        )
        if direction == "중심":
            return f"{region_name} 중심부 포함"
        else:
            return f"{region_name} {direction} 포함"

    # 중심을 찾지 못한 경우
    return f"{region_name} 일부 포함"

def query_regions_in_rect(features, rect_coords, only_representive_text = False) -> dict:
    """
    사각형 영역(rect_coords)에 포함되는 행정구역들을 반환.

    Parameters:
    - features: load_features의 반환값
    - rect_coords: [[lon1, lat1], [lon2, lat2], [lon3, lat3], [lon4, lat4]] 형태의 사각형 좌표

    Returns:
    - dict: {
        "representative": [...],  # 광역 단위 대표 표현
        "fully_contained": [...],  # 완전히 포함된 지역
        "all_regions": [...],  # 완전 + 일부 포함 (중복 제거)
        "center": [lon, lat],  # 중심 좌표
        "distance_info": None or [...]  # 범위 밖이면 거리 정보
    }
    """
    # 사각형 Polygon 생성
    if len(rect_coords) < 4:
        raise ValueError("rect_coords는 4개 이상의 좌표를 가져야 합니다.")
    elif len(rect_coords) > 4:
        rect_coords = rect_coords[:4]

    rect_polygon = Polygon(rect_coords)
    if not rect_polygon.is_valid:
        rect_polygon = make_valid(rect_polygon)

    # 중심 좌표 계산
    centroid = rect_polygon.centroid
    center_lon, center_lat = centroid.x, centroid.y

    fully_contained = []  # 완전히 포함된 지역
    partially_contained = []  # 일부 포함된 지역
    provincial_regions = {}  # 광역 단위별 포함 정보 {name: coverage_ratio}
    region_centers_cache = {}  # 광역 단위 중심 좌표 캐시

    for feature_data in features:
        # 이전 버전 호환성 처리
        if len(feature_data) >= 5:
            g, pg, nm, all_names, center_coords = feature_data
        else:
            g, pg, nm, all_names = feature_data[:4]
            center_coords = None
        # 교차 판정
        if not rect_polygon.intersects(g):
            continue

        # NAME_KEYS에서 답변 레벨에 해당하는 이름들만 추출
        valid_names = []
        for name in all_names:
            if is_answer_level(name):
                valid_names.append(name)

        if not valid_names:
            continue

        # 완전 포함 vs 일부 포함 판정
        intersection = rect_polygon.intersection(g)
        intersection_area = intersection.area
        region_area = g.area

        # 포함 비율 계산
        coverage_ratio = (intersection_area / region_area) if region_area > 0 else 0

        # 거의 완전히 포함된 경우 (99% 이상)
        is_full = coverage_ratio > 0.99

        for name in valid_names:
            # 광역 단위 정보 수집 (면적 비율 저장)
            if is_provincial_level(name):
                if name not in provincial_regions:
                    provincial_regions[name] = coverage_ratio
                else:
                    # 이미 있으면 더 큰 비율로 업데이트
                    provincial_regions[name] = max(provincial_regions[name], coverage_ratio)

            # 완전/일부 포함 분류
            if is_full:
                if name not in fully_contained:
                    fully_contained.append(name)
            else:
                if name not in partially_contained:
                    partially_contained.append(name)

    # 중복 제거: fully_contained에 있으면 partially_contained에서 제거
    # partially_contained = [name for name in partially_contained if name not in fully_contained]

    # 광역 단위 대표 표현 생성
    representative = []
    for region_name, coverage_ratio in provincial_regions.items():
        rep_name = get_region_representative_name(
            features, region_name, coverage_ratio, center_lon, center_lat, region_centers_cache
        )
        representative.append(rep_name)

    # 정렬
    fully_contained = sort_by_admin_level(fully_contained)
    # partially_contained = sort_by_admin_level(partially_contained)
    representative = sort_by_admin_level(representative)

    # 전체 지역 (완전 + 일부)
    all_regions = sort_by_admin_level(list(set(fully_contained + partially_contained)))

    # 결과가 없으면 중심점 기준으로 거리 정보를 대표 표현으로 반환
    if not all_regions:
        distance_info = find_nearest_region_info(features, center_lon, center_lat)
        representative = distance_info if distance_info else []

    if only_representive_text:
        return {"representative": ", ".join(representative)}

    return {
        "representative": representative,
        "fully_contained": fully_contained,
        # "partially_contained": partially_contained,
        "all_regions": all_regions,
        "center": [center_lon, center_lat],
        "distance_info": None  # 이제 representative에 포함됨
    }


class Rect2Region():
    def __init__(self, files=None):
        if files == None:
            BASE_PATH = r"C:\Users\T3Q\jeonghan\Eunhyea_Assist\geo_map\using_data"
            files = (
                os.path.join(BASE_PATH, "boundaries_KR_20220407.geojson"),
                os.path.join(BASE_PATH, "new_prk_admbnda_adm2_wfp_20190624.geojson")
            )
            
        self.features = load_features(files)

        self.test_idx = 0
    
    def convert(self,rect_coords, only_representive_text = False):
        result = query_regions_in_rect(self.features, rect_coords, only_representive_text = only_representive_text)
        return result

    def convert_many(self,rect_coords_list, only_representive_text = False):
        result = []
        for rect in rect_coords_list:
            result.append(self.convert(rect, only_representive_text = only_representive_text))
        return result
    
    def show(self, result):
        print("=" * 80)
        print(f"테스트 {self.test_idx}")
        print("=" * 80)
        print(f"사각형 좌표: {rect_coords}")
        print(f"중심 좌표: {result['center']}")
        print()
        print(f"광역 단위 대표 표현: {result['representative']}")
        print(f"완전히 포함된 지역: {result['fully_contained']}")
        print(f"전체 지역 (완전+일부): {result['all_regions']}")
        print()
        self.test_idx += 1

    def convert_json_file(self, input_file, output_file):
        """
        경고!!!: 특정 스키마로 고정된 함수임. 스키마 권토 권고.

        data.json의 region_text를 변환하여 converted_data.json 생성

        Parameters:
        - input_file: 입력 JSON 파일 경로
        - output_file: 출력 JSON 파일 경로
        """
        import json

        # data.json 읽기
        print("데이터를 읽는 중...")
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # hits.hits 배열 처리
        total_hits = len(data['hits']['hits'])
        print(f"총 {total_hits}개의 항목을 처리합니다...")

        for idx, hit in enumerate(data['hits']['hits']):
            if (idx + 1) % 100 == 0:
                print(f"진행 중: {idx + 1}/{total_hits}")

            # region_text 가져오기
            region_text = hit['_source'].get('region_text')

            if region_text:
                # JSON 문자열을 파싱
                if isinstance(region_text, str):
                    region_coords = json.loads(region_text)
                else:
                    region_coords = region_text

                # 첫 4개 좌표만 슬라이싱 (N,2) 형태의 리스트에서
                rect_coords = region_coords[:4]

                # converter.convert 호출
                result = self.convert(rect_coords)

                # representative 리스트를 ", "로 조인
                converted_text = ", ".join(result['representative'])

                # region_text 대체
                hit['_source']['region_text'] = converted_text

        # 변환된 데이터를 새 파일로 저장
        print("변환된 데이터를 저장하는 중...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"완료! 변환된 데이터가 {output_file}에 저장되었습니다.")


    def get_region_boundary(self, region_name):
        """
        특정 행정구역 이름을 입력하면 경계 좌표 및 중심 좌표를 반환.

        Parameters:
        - features: load_features의 반환값
        - region_name: 찾고자 하는 행정구역 이름 (예: "서울특별시", "강남구", "평양시")

        Returns:
        - dict: {
            "found": True/False,
            "name": 찾은 행정구역 이름,
            "bounds": [min_lon, min_lat, max_lon, max_lat],  # 경계 박스
            "center": [lon, lat],  # 중심 좌표
            "boundary_coords": [[lon1, lat1], [lon2, lat2], ...]  # 실제 경계 좌표들
        }
        - 찾지 못한 경우: {"found": False}
        """
        for feature_data in self.features:
            # 이전 버전 호환성 처리
            if len(feature_data) >= 5:
                g, pg, nm, all_names, center_coords = feature_data
            else:
                g, pg, nm, all_names = feature_data[:4]
                center_coords = None

            # all_names에서 매칭되는 이름 찾기
            if region_name in all_names:
                # 경계 박스
                minx, miny, maxx, maxy = g.bounds

                # 중심 좌표
                centroid = g.centroid
                center_lon, center_lat = centroid.x, centroid.y

                # 경계 좌표 추출
                boundary_coords = []
                if g.geom_type == 'Polygon':
                    boundary_coords = list(g.exterior.coords)
                elif g.geom_type == 'MultiPolygon':
                    # MultiPolygon의 경우 가장 큰 폴리곤 선택
                    largest_polygon = max(g.geoms, key=lambda p: p.area)
                    boundary_coords = list(largest_polygon.exterior.coords)

                # 좌표를 [lon, lat] 형식으로 변환
                boundary_coords = [[coord[0], coord[1]] for coord in boundary_coords]

                return {
                    "found": True,
                    "name": region_name,
                    "bounds": [minx, miny, maxx, maxy],
                    "center": [center_lon, center_lat],
                    "boundary_coords": boundary_coords
                }

        return {"found": False}


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
    input_file = r"C:\Users\T3Q\jeonghan\Eunhyea_Assist\geo_map\using_data\data.json"
    output_file = r"C:\Users\T3Q\jeonghan\Eunhyea_Assist\geo_map\using_data\converted_data.json"
    converter.convert_json_file(input_file, output_file)
