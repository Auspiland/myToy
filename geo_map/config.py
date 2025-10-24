import sys
import os

# 프로젝트 루트 경로 설정
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# 시스템 경로에 추가 (geo_map을 기준으로 import 가능하도록)
if BASE_PATH not in sys.path:
    sys.path.insert(0, BASE_PATH)

# 환경변수로도 접근 가능하도록 설정
os.environ["BASE_PATH"] = BASE_PATH
print(BASE_PATH)