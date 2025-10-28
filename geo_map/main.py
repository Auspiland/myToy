import time
from config import BASE_PATH
from core.rect2region import Rect2Region
import os

converter = Rect2Region()

t0 = time.time()

# 테스트 케이스 1: 사용자 제공 좌표
rect_coords = [
    [126.58944268582343, 33.41526082433313],
    [126.58944268582343, 33.41526082433313],
    [126.58944268582343, 33.41526082433313],
    [126.58944268582343, 33.41526082433313]
]

result1 = converter.convert(rect_coords)
# converter.show(result1)
# output_path = os.path.join(BASE_PATH, "static", "test_1.geojson")
# converter.create_geojson(rect_coords, output_path, result=result1, openbrowser=True)





# # 테스트 케이스 2: 서울 전체를 포함하는 사각형
rect_coords_seoul = [
    [126.7, 37.7],
    [127.3, 37.7],
    [126.7, 37.4],
    [127.3, 37.4]
]

result2 = converter.convert(rect_coords_seoul)
# converter.show(result2)
# output_path2 = os.path.join(BASE_PATH, "static", "test_2.geojson")
# converter.create_geojson(rect_coords_seoul, output_path2, result=result2, openbrowser=True)






# 테스트 케이스 3: 바다 한가운데 (범위 밖)
rect_coords_ocean = [
    [120.0, 35.0],
    [121.0, 35.0],
    [120.0, 34.0],
    [121.0, 34.0]
]

result3 = converter.convert(rect_coords_ocean)
# converter.show(result3)
# output_path3 = os.path.join(BASE_PATH, "static", "test_3.geojson")
# converter.create_geojson(rect_coords_ocean, output_path3, result=result3, openbrowser=True)

gap = time.time()-t0
print(f"Upper tests processing time (includes initializing time) : {gap:.5f}s")
print()


print("=" * 80)

result4 = converter.get_region_boundary("서울특별시")
print(result4['name'])
print(result4['bounds'])
print(result4['center'])

print("=" * 80)
print("JSON 파일 변환 예제")
print("=" * 80)





# JSON 파일 변환 실행
t0 = time.time()
using_data_path = os.path.join(BASE_PATH, "using_data")
input_file = os.path.join(using_data_path, "data.json")
output_file = os.path.join(using_data_path, "converted_data.json")
converter.convert_json_file(input_file, output_file)
gap = time.time()-t0
print(f"{gap:.5f}s")

