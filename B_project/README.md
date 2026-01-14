# B_project

알고리즘 및 코딩 테스트 관련 프로젝트입니다.

<!-- AUTO-UPDATE:START -->
<!-- 이 섹션은 GitHub Actions에 의해 자동으로 업데이트됩니다 -->
## 프로젝트 구성

### boj_bible
백준 알고리즘 문제 해결을 위한 파이썬 라이브러리입니다.

- **basic**: 기본 자료구조 (스택, 큐, 링크드 리스트, Union-Find, Heap)
- **graph**: 그래프 알고리즘 (BFS, DFS, 최단경로, 위상정렬)
- **tree**: 트리 알고리즘 (세그먼트 트리, LCA)
- **string**: 문자열 알고리즘 (패턴 매칭, Trie)
- **advanced**: 고급 알고리즘 (네트워크 플로우)

### CT (Coding Test)
코딩 테스트 자동화 및 기록 관련 도구입니다.

- 변경 사항(요약): B_project/CT/auto_solve/common_utils.py에서 LLM 관련 함수들의 기본 모델 파라미터가 "gpt-5"에서 "gpt-5-nano"로 변경되었습니다.
  - 영향을 받는 함수: response_GPT, response_GPT_stream, response_GPT_with_stream_fallback
  - 영향: model 인자를 생략하고 호출하던 기존 코드들은 이제 기본적으로 "gpt-5-nano"를 사용하게 됩니다. 특정 모델(예: gpt-5)을 계속 사용하려면 model 파라미터를 명시적으로 지정하세요.

- 추가 파일: B_project/CT/kakao_history.ipynb
  - 내용 요약: 노트북에 세 가지 문제 풀이 함수(파이썬 코드 셀)가 포함되어 있습니다.
    1. solution(n, infection, edges, k)
       - 설명: 간선 타입별로 연결요소를 비트마스크로 미리 계산한 뒤, 상태(감염된 노드 집합)를 비트마스크로 표현하여 단계(k) 이내에 감염 가능한 최대 노드 수를 BFS로 탐색하는 알고리즘입니다. 각 단계에서 타입 1/2/3 중 하나를 선택해 해당 타입에서 연결요소 전체가 전염되는 방식으로 상태 전이가 일어납니다.
       - 시간 복잡도: 전처리(간선 타입별 연결요소 계산)는 O(n + m). 상태 탐색은 상태 공간(최악의 경우 2^n)에 비례하므로 지수적(최악: O(2^n * n))이며, 실제 성능은 n이 작을 때(예: n ≤ 20 등) 적절합니다.
       - 반환값: k 단계 이내에 달성 가능한 최대 감염 노드 수(정수).
    2. solution(dist_limit: int, split_limit: int) -> int
       - 설명: 거리(분할) 예산 D와 한 경로에서 허용되는 분기 상한 S를 받아, 2-분기와 3-분기를 조합해 만들 수 있는 말단(leaf) 노드의 최대 개수를 시뮬레이션으로 계산합니다. 2^b * 3^a ≤ S 조건을 사용해 가능한 분기 조합을 탐색하고, 각 조합에 대해 D 예산을 사용해 레벨별 분할을 적용합니다.
       - 시간 복잡도: p2/p3 길이(≈ log S)와 각 시뮬레이션이 최대 D 단계 만큼 수행되므로 O((log S) * D) 수준으로 예측됩니다.
       - 반환값: 주어진 제약에서 얻을 수 있는 leaf(말단 노드) 최대값(정수).
    3. solution(signals)
       - 설명: 여러 신호등(signal)들의 (초기 초당) 녹색 G_i, 노란 Y_i, 적색 R_i 값을 입력받아, 모든 신호등이 동시에 '노란불'이 되는 가장 이른 시각 t(>=1)를 찾는 문제 풀이 함수입니다. 각 신호등의 주기 P_i = G_i + Y_i + R_i이며, 시각 t에서 (t-1) % P_i 가 [G_i, G_i + Y_i - 1] 범위이면 그 신호등은 '노란불'입니다. 알고리즘은 첫 번째 신호등의 노란불 시작 시간들만 후보로 고려하고, 각 후보에 대해 그 주기(P0) 단위로 건너뛰며 전체 신호등을 검사합니다. 전체 패턴이 반복되는 초주기 L = lcm(P_i)까지만 검사하면 충분합니다.
       - 시간 복잡도: 초주기 L에 대해 최악 O(L * n) (각 후보 시각마다 모든 신호등을 검사). 실무 제약(예: n ≤ 5, P_i ≤ 20 등)이면 L ≤ 55440 정도로 전수 탐색이 가능해 빠르게 동작합니다.
       - 공간 복잡도: O(1) 추가 메모리(상수).
       - 반환값: 모든 신호등이 동시에 노란불인 가장 작은 시각 t(정수). 존재하지 않으면 -1을 반환.
  - 주의: 노트북(.ipynb)이므로 바로 import 가능한 .py로 변환하여 사용하거나, 노트북의 코드 셀을 복사해 모듈화해서 사용하세요.

- 추가 파일: B_project/special_prompt.md
  - 내용 요약: FastAPI 기반 비동기 백엔드, PostgreSQL(Async), Redis, Docker Compose, GitLab CI/CD 등으로 구성된 "AI 포털" 프로젝트의 상세 문서(설치/구성/개발 규칙/배포/문서화 가이드 등). 백엔드 표준(Async, SQLAlchemy 2.0, Pydantic v2), 개발 워크플로우, Docker/CI 설정, 문서화 규칙 등이 포함되어 있습니다.
  - 영향: 프로젝트 전반의 운영·개발 가이드 문서로 참조용이며 코드 동작에는 직접적인 변경을 주지 않습니다.

사용 예시 (Python):
```python
from B_project.CT.auto_solve.common_utils import (
    response_GPT,
    response_GPT_stream,
    response_GPT_with_stream_fallback,
)

# 기본 사용: model 파라미터를 지정하지 않으면 'gpt-5-nano'가 사용됩니다.
text = response_GPT(system_prompt="시스템 메시지", user_prompt="사용자 질문")
print(text)

# 모델을 명시적으로 지정하려면:
text = response_GPT(system_prompt="", user_prompt="질문 내용", model="gpt-5")
print(text)

# 스트리밍 사용 예시:
for chunk in response_GPT_stream([{"role": "user", "content": "스트리밍 테스트"}]):
    print(chunk)

# 스트리밍 폴백을 사용하는 호출 예시:
result = response_GPT_with_stream_fallback(user_prompt="입력", max_retries=2, fallback_stream=True)
print(result)
```

사용 예시 (kakao_history 노트북에 포함된 함수 사용 예 — 노트북 코드를 모듈화했을 경우):
```python
# 예시 1: infection 문제
# 그래프: n 노드, edges = [(x,y,t), ...], 초기 감염 정점 infection(1-based), 최대 단계 k
n = 6
infection = 1
edges = [
    (1, 2, 1),
    (2, 3, 2),
    (3, 4, 3),
    (4, 5, 1),
    (5, 6, 2),
]
k = 2
# from B_project.CT.kakao_history import solution as solution_infection
# print(solution_infection(n, infection, edges, k))

# 예시 2: 분할(leaf 최대화) 문제
dist_limit = 5
split_limit = 12
# from B_project.CT.kakao_history import solution as solution_leaves
# print(solution_leaves(dist_limit, split_limit))

# 예시 3: 신호등(동시 노란불) 문제
# signals: [(G1, Y1, R1), (G2, Y2, R2), ...]
signals = [
    (2, 1, 3),  # 신호등 1: G=2, Y=1, R=3 -> 주기 6
    (1, 2, 2),  # 신호등 2: G=1, Y=2, R=2 -> 주기 5
]
# from B_project.CT.kakao_history import solution as solution_signals
# print(solution_signals(signals))  # 모든 신호등이 동시에 노란불이 되는 가장 이른 시각 또는 -1
```

주의 사항:
- 기본 모델 변경은 응답 지연, 응답 품질, 비용에 영향을 줄 수 있습니다. 필요에 따라 model 인자를 명시하여 원하는 모델을 사용하세요.
- B_project/CT/kakao_history.ipynb 및 B_project/special_prompt.md 파일이 새로 추가되었습니다. 노트북의 코드를 재사용하려면 .py로 추출하거나 내용 일부를 모듈화해 사용하시기 바랍니다.
- 이 README의 나머지 부분(알고리즘 목록 등)은 변경되지 않았습니다.
<!-- AUTO-UPDATE:END -->

---



<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 9efe861a1d5c671f0273038934e263aacb0b1c12 -->
