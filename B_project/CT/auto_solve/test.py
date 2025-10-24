import os, sys, time, logging
from common_utils import response_GPT
from gen_data import main as generate_data
from test_utils import evaluate_jsonl
from debug import analysing_error
from dotenv import load_dotenv

load_dotenv()
BASE_PATH = os.getenv("BASE_PATH")
file_dir = os.path.join(BASE_PATH, "B_project","CT","auto_solve","generated_data")

log = logging.getLogger(__name__)

problem = """
세계적인 도둑 상덕이는 보석점을 털기로 결심했다.

상덕이가 털 보석점에는 보석이 총 N개 있다. 각 보석은 무게 Mi와 가격 Vi를 가지고 있다. 상덕이는 가방을 K개 가지고 있고, 각 가방에 담을 수 있는 최대 무게는 Ci이다. 가방에는 최대 한 개의 보석만 넣을 수 있다.

상덕이가 훔칠 수 있는 보석의 최대 가격을 구하는 프로그램을 작성하시오.

입력
N과 K가 주어진다. (1 ≤ N, K ≤ 300,000)

jewerly 리스트 N개의 줄에는 각 보석의 정보 Mi와 Vi가 주어진다. (0 ≤ Mi, Vi ≤ 1,000,000)

bag 리스트에는 K개의 가방에 담을 수 있는 최대 무게 Ci가 주어진다. (1 ≤ Ci ≤ 100,000,000)

모든 숫자는 양의 정수이다.

출력
최대 가격 (int)

solution(N, K, jewerly, bag)

jewerly.shape = (2,N)
bag.shape = (K)
"""

# 테스트 데이터를 생성하는데 조심할 특별 지침
special_prompt="""
모든 숫자는 0 이상의 정수, invalid 예시 없음.
"""

import bisect

def solution(N, K, jewerly, bag):

    N = int(N)
    K = int(K)

    jewerly.sort(key=lambda x: x[1], reverse=True)

    bag.sort()
    bag_mask = [0]*K

    total = 0

    for weight, price in jewerly:
        
        idx = bisect.bisect_left(bag, weight)
        while idx < len(bag):
            if bag_mask[idx] == 1:
                idx += 1
            else:
                total += price
                bag_mask[idx] = 1
                break
        
    return total





def debugging():
    code = """
import bisect

def solution(N, K, jewerly, bag):

    N = int(N)
    K = int(K)

    jewerly.sort(key=lambda x: x[1], reverse=True)

    bag.sort()

    sum = 0

    for weight, price in jewerly:
        
        idx = bisect.bisect_left(bag, weight)
        if not idx == len(bag):
            bag.pop(idx)
            sum += price
        
    return sum
"""
    err_msg = r"""
[1] 입력: {"N":3,"K":2,"jewerly":[[1,2,3],[10,20,30]],"bag":[2,3]}
예상: 50
출력: Exception: too many values to unpack (expected 2)
Traceback (most recent call last):
  File "C:\Users\T3Q\jeonghan\my_github\myToy\B_project\CT\auto_solve\test_utils.py", line 91, in evaluate_jsonl
    pred = solution(*args, **kwargs)
  File "C:\Users\T3Q\jeonghan\my_github\myToy\B_project\CT\auto_solve\test.py", line 57, in solution
    for weight, price in jewerly:
        ^^^^^^^^^^^^^
ValueError: too many values to unpack (expected 2)

시간: 0.00ms
tags: ['err']
note: 대체 스키마: jewerly를 2xN 행렬로 표현
---
[2] 입력: {"N":5,"K":3,"jewerly":[[0,100],[1,100],[1,99],[0,98],[2,1000]],"bag":[1,1,1]}
예상: 297
출력: 299
시간: 0.00ms
tags: ['corner']
note: 무게 0과 1 혼합, 무거운 보석은 끝까지 미적합
---
[3] 입력: {"N":4,"K":3,"jewerly":[[0,2,1,1],[5,0,10,10]],"bag":[1,2,2]}
예상: 25
출력: Exception: too many values to unpack (expected 2)
Traceback (most recent call last):
  File "C:\Users\T3Q\jeonghan\my_github\myToy\B_project\CT\auto_solve\test_utils.py", line 91, in evaluate_jsonl
    pred = solution(*args, **kwargs)
  File "C:\Users\T3Q\jeonghan\my_github\myToy\B_project\CT\auto_solve\test.py", line 57, in solution
    for weight, price in jewerly:
        ^^^^^^^^^^^^^
ValueError: too many values to unpack (expected 2)
"""
    print(analysing_error(problem=problem, code=code, error_msg=err_msg, special_prompt=special_prompt))



if __name__ == "__main__":
    # data_path = generate_data(problem_text=problem, special_prompt=special_prompt)

    data_path = os.path.join(file_dir, "세계적인 도둑 상.jsonl")
    
    evaluate_jsonl(data_path, solution=solution)

    # debugging()


