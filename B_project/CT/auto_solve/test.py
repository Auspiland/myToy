import os, sys, time, logging
from common_utils import response_GPT
from gen_data import main as generate_data
from test_utils import evaluate_jsonl
from debug import analysing_error

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

    sum = 0

    for weight, price in jewerly:
        
        idx = bisect.bisect_left(bag, weight)
        if not idx == len(bag):
            bag.pop(idx)
            sum += price
        
    return sum




def debugging():
    code = """

"""
    print(analysing_error(problem=problem, code=code, error_msg=err_msg, special_prompt=special_prompt))


if __name__ == "__main__":
    # data_path = generate_data(problem_text=problem, special_prompt=special_prompt)

    data_path = r"C:\_mangojelly\Git-mytoy\myToy\B_project\CT\auto_solve\generated_data\세계적인 도둑 상.jsonl"
    
    evaluate_jsonl(data_path, solution=solution)

    # debugging()


