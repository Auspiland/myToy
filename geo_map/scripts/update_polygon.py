import os
import sys
import requests
import json
import time
import logging
from dotenv import load_dotenv

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import BASE_PATH
from scripts.common_constants import KR_CENTER_LON, KR_CENTER_LAT, MAX_API_RETRIES

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# 환경 변수 로드
env_path = os.path.join(BASE_PATH, "src", ".env")
load_dotenv(env_path)
V_KEY = os.getenv("V_WORLD_API_KEY")

if not V_KEY:
    logger.error("V_WORLD_API_KEY not found in environment variables")
    raise ValueError("V_WORLD_API_KEY is required. Please check your .env file.")

# 파일 경로
USING_DATA_PATH = os.path.join(BASE_PATH, "using_data")
boundaries_file = os.path.join(USING_DATA_PATH, "boundaries_KR_20220407.geojson")
output_file = os.path.join(USING_DATA_PATH, "boundaries_KR_20220407_updated.geojson")

# 특정 지역만 업데이트 (None이면 전체)
TARGET_REGION = None  # None으로 설정하면 전체 업데이트

logger.info(f"Loading boundaries file: {boundaries_file}")
with open(boundaries_file, 'r', encoding='utf-8') as f:
    boundaries_data = json.load(f)

# admin_level 4인 지역 찾기 (특별시/광역시/도)
level4_features = [f for f in boundaries_data['features'] if f['properties']['admin_level'] == 4]
logger.info(f"Found {len(level4_features)} admin_level 4 regions")

if TARGET_REGION:
    logger.info(f"Target region: {TARGET_REGION}")


def fetch_geometry_with_retry(url, key, lon, lat, max_retries=MAX_API_RETRIES):
    """
    Point를 재조정하면서 geometry를 가져오는 함수
    실패 시 대한민국 중심점 방향으로 이동하면서 재시도

    Args:
        url: V-World API URL
        key: API 키
        lon: 경도
        lat: 위도
        max_retries: 최대 재시도 횟수

    Returns:
        tuple: (geometry, success, retry_count)
    """

    # 현재 point에서 대한민국 중심으로의 방향 벡터
    dir_lon = KR_CENTER_LON - lon
    dir_lat = KR_CENTER_LAT - lat

    # 방향 정규화 (거리 계산)
    import math
    distance = math.sqrt(dir_lon**2 + dir_lat**2)
    if distance > 0:
        dir_lon = dir_lon / distance
        dir_lat = dir_lat / distance

    # 재시도를 위한 offset 값들 - 대한민국 중심 방향 우선
    offsets = [
        (0, 0),                           # 원본
        (dir_lon * 0.05, dir_lat * 0.05), # 중심 방향으로 0.05도
        (dir_lon * 0.1, dir_lat * 0.1),   # 중심 방향으로 0.1도
        (dir_lon * 0.15, dir_lat * 0.15), # 중심 방향으로 0.15도
        (dir_lon * 0.2, dir_lat * 0.2),   # 중심 방향으로 0.2도
        (dir_lon * 0.3, dir_lat * 0.3),   # 중심 방향으로 0.3도
        (0.05, 0),                        # 동쪽
        (-0.05, 0),                       # 서쪽
        (0, 0.05),                        # 북쪽
        (0, -0.05),                       # 남쪽
    ]

    for i, (offset_lon, offset_lat) in enumerate(offsets[:max_retries]):
        adjusted_lon = lon + offset_lon
        adjusted_lat = lat + offset_lat

        if i > 0:
            logger.debug(f"  [RETRY {i}] Adjusting point to ({adjusted_lon}, {adjusted_lat})")

        params = {
            "service": "data",
            'request': 'GetFeature',
            'data': 'LT_C_ADSIDO_INFO',
            'key': key,
            'size': '100',
            'geomFilter': f'POINT({adjusted_lon} {adjusted_lat})'
        }

        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data_json = response.json()

                if data_json.get("response", {}).get("status") == "OK":
                    feature_collection = data_json["response"]["result"]["featureCollection"]

                    if feature_collection.get("features") and len(feature_collection["features"]) > 0:
                        return feature_collection["features"][0]["geometry"], True, i
                    else:
                        logger.debug(f"      No features at this point")
                else:
                    logger.debug(f"      API status: {data_json.get('response', {}).get('status')}")
            else:
                logger.warning(f"      HTTP status: {response.status_code}")

            time.sleep(0.5)

        except Exception as e:
            logger.error(f"      Error: {e}")
            time.sleep(0.5)

    return None, False, max_retries


# V-World API를 사용하여 각 지역의 geometry 가져오기
url = "https://api.vworld.kr/req/data"
updated_count = 0
failed_regions = []

for feature in boundaries_data['features']:
    if feature['properties']['admin_level'] != 4:
        continue

    name = feature['properties']['name']
    name_en = feature['properties'].get('name_en', '')

    # TARGET_REGION이 설정되어 있으면 해당 지역만 처리
    if TARGET_REGION and name_en != TARGET_REGION:
        continue

    center_lon = feature['properties']['center_lon']
    center_lat = feature['properties']['center_lat']

    logger.info(f"\nFetching geometry for: {name} ({name_en})")
    logger.info(f"  Center point: ({center_lon}, {center_lat})")

    geometry, success, retry_count = fetch_geometry_with_retry(
        url, V_KEY, center_lon, center_lat
    )

    if success:
        feature['geometry'] = geometry
        updated_count += 1
        if retry_count > 0:
            logger.info(f"  [OK] Updated successfully (after {retry_count} retries)")
        else:
            logger.info(f"  [OK] Updated successfully")
    else:
        logger.error(f"  [FAIL] Could not fetch geometry after {retry_count} attempts")
        failed_regions.append(name)

logger.info(f"\n{'='*60}")
logger.info(f"Total {updated_count} regions updated successfully")

if failed_regions:
    logger.warning(f"\nFailed regions ({len(failed_regions)}):")
    for region in failed_regions:
        logger.warning(f"  - {region}")

# 수정된 데이터 저장
logger.info(f"\nSaving updated data to: {output_file}")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(boundaries_data, f, ensure_ascii=False, indent=2)

logger.info("Done!")
