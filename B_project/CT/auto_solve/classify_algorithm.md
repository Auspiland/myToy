# 그리디 (Greedy)

## 개념

* 매 단계에서 **국소 최적(가장 좋아 보이는 선택)**을 하고, 그 누적 결과가 전체 최적이 되도록 설계합니다.
* 성립 조건: **탐욕적 선택 속성**(국소 최적 ⇒ 전역 최적 보장), **최적 부분 구조**(부분문제의 최적해로 전체 최적해 구성).

## 언제 쓰나

* 간격 스케줄링(가장 빨리 끝나는 일부터), 활동 선택, 동전 거스름(표준 화폐계), 로프/회의실 배정, 허프만 코딩, 일부 MST(Prim/Kruskal).

## 파이썬 패턴

### 1) 활동 선택(끝나는 시간 기준 정렬)

```python
def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])   # (start, end)
    cnt, end = 0, -10**18
    for s, e in intervals:
        if s >= end:
            cnt += 1
            end = e
    return cnt
```

* 복잡도: 정렬 O(n log n) + 선형 스캔 O(n) ⇒ **O(n log n)**

### 2) 우선순위 큐 기반 그리디

```python
import heapq

def assign_rooms(meetings):
    meetings.sort()   # 시작시간 기준
    heap = []         # 끝나는 시간 최소 힙
    for s, e in meetings:
        if heap and heap[0] <= s:
            heapq.heapreplace(heap, e)  # 기존 방 재사용
        else:
            heapq.heappush(heap, e)     # 새 방
    return len(heap)
```

* 복잡도: 정렬 O(n log n) + 힙연산 O(n log n)

## 실전 팁/주의

* 반례 검증: 동전 거스름은 **모든 화폐 체계**에서 그리디가 최적이 아닙니다(예: 1,3,4 단위에서 6).
* 그리디의 정당성은 **교환 논증(exchange argument)**로 자주 증명합니다.

---

# 구현 (Implementation / Simulation)

## 개념

* 특별한 알고리즘보다 **요구사항을 그대로 코드로 옮기는 시뮬레이션/구현 문제**.
* 문자열 파싱, 좌표 시뮬레이션, 상태 머신, 규칙 처리.

## 파이썬 패턴

### 1) 2D 격자 시뮬레이션

```python
# 4방향 이동
DIR4 = [(1,0), (-1,0), (0,1), (0,-1)]

def in_range(r, c, H, W):
    return 0 <= r < H and 0 <= c < W

def simulate(board, start):
    H, W = len(board), len(board[0])
    r, c = start
    for dr, dc in DIR4:
        nr, nc = r + dr, c + dc
        if in_range(nr, nc, H, W) and board[nr][nc] != '#':
            # move or act
            pass
```

### 2) 문자열/토큰 처리

```python
import re
tokens = re.findall(r"[A-Za-z]+|\d+|[^\w\s]", line)
```

## 복잡도

* 대부분 **입력 크기만큼**(문자열/배열 순회) ⇒ `O(n)` 또는 `O(nm)`.

## 실전 팁

* I/O가 큰 경우 `sys.stdin.readline` 사용.
* 경계/오프바이원 오류가 빈번 → `in_range` 유틸로 통일.
* 시뮬레이션은 **상태 정의**(좌표, 방향, 남은 체력…)와 **전이 규칙**을 표로 먼저 적으면 실수 감소.

---

# DFS/BFS

## 개념

* **DFS**: 깊이 우선(스택/재귀). 경로 탐색, 순환 검출, 위상정렬 보조, 연결요소.
* **BFS**: 너비 우선(큐). **가중치가 동일(또는 1)인 그래프 최단 거리**.

## 파이썬 패턴

### 1) DFS (재귀/스택)

```python
import sys
sys.setrecursionlimit(1_000_000)

def dfs_rec(u, adj, seen):
    seen[u] = True
    for v in adj[u]:
        if not seen[v]:
            dfs_rec(v, adj, seen)

def dfs_iter(start, adj):
    seen, stack = set(), [start]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        stack.extend(adj[u])
    return seen
```

### 2) BFS (큐: collections.deque)

```python
from collections import deque

def bfs(start, adj):
    dist = {start: 0}
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist
```

## 복잡도

* 인접 리스트 기준 **O(V+E)**, 공간 **O(V)**.

## 실전 팁

* 파이썬 재귀는 깊게 들어가면 `RecursionError` → 가능하면 **반복 DFS** 사용.
* 격자 BFS는 **방문 체크를 큐에 넣을 때** 수행해야 중복 삽입 방지.

---

# 정렬 (Sorting)

## 개념 & 파이썬 기본

* 파이썬 내장 정렬은 **Timsort**: 실무적으로 매우 빠르고 **stable**.
* `sorted(iterable, key=..., reverse=...)` / `list.sort(...)`

## 패턴

### 1) 다중 키 정렬(안정성 활용)

```python
# (국어 내림, 영어 오름, 수학 내림)
arr.sort(key=lambda x: (-x.kor, x.eng, -x.math))
```

### 2) 커스텀 비교(권장 X, 필요시)

```python
from functools import cmp_to_key
def cmp(a, b): ...
arr.sort(key=cmp_to_key(cmp))
```

### 3) 계수 정렬(키 범위가 작을 때)

```python
def counting_sort(a, K):
    cnt = [0]*(K+1)
    for x in a:
        cnt[x] += 1
    out = []
    for v in range(K+1):
        out.extend([v]*cnt[v])
    return out
```

## 복잡도

* 비교기반 정렬 하한: **Ω(n log n)**
* Timsort 평균/최악: **O(n log n)**, 공간 **O(n)**(부분적으로 in-place)
* 계수/버킷/기수: 키가 제한적이면 **O(n + K)** 가능.

## 실전 팁

* **Stable**을 이용해 “보조 키로 먼저 정렬 → 주 키로 정렬” 트릭 가능.
* 대용량 정렬에서 키 함수는 **가볍게**(필요시 사전 계산으로 캐시).

---

# 이진 탐색 (Binary Search)

## 개념

* 정렬/단조 성질이 있을 때 **로그 시간**으로 위치나 답을 찾는 방법.
* 수열뿐 아니라, **불/참으로 단조 변화하는 해 공간**에도 적용(Parametric Search).

## 파이썬 패턴

### 1) 위치 탐색(bisect)

```python
from bisect import bisect_left, bisect_right

a = [1,2,2,2,3,5]
i = bisect_left(a, 2)   # 2의 첫 위치(왼 경계)
j = bisect_right(a, 2)  # 2의 끝 다음(오 경계)
count_2 = j - i
```

### 2) 답(최소/최대) 탐색(단조 판별 함수 ok)

```python
def binary_search_min(lo, hi, ok):
    # 최소 인덱스 s.t. ok(x) True, [lo, hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### 3) 실수 영역(허용 오차)

```python
def binary_search_real(lo, hi, ok, eps=1e-9):
    for _ in range(100):   # 충분한 반복
        mid = (lo + hi) / 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi
```

## 복잡도

* 검사 함수가 `T(x)`면 총 **O(T(x) · log R)** (`R`은 탐색 범위 크기).

## 실전 팁

* **무한 루프** 방지(조건 `lo < hi`)와 중앙값 갱신 주의.
* 정렬이 안 된 배열에는 직접 적용 불가(단, **매개변수 탐색**은 가능).

---

# 다이나믹 프로그래밍 (DP)

## 개념

* **중복 부분문제 + 최적 부분 구조**일 때, 결과를 저장하며 계산.
* 방식: **Top-Down(메모이제이션)**, **Bottom-Up(테이블링)**.

## 파이썬 패턴

### 1) Top-Down with `lru_cache`

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def f(n):
    if n <= 1:
        return n
    return f(n-1) + f(n-2)
```

### 2) 1로 만들기(최소 연산 수, Bottom-Up 예)

```python
def make_one(n):
    dp = [0]*(n+1)
    for i in range(2, n+1):
        dp[i] = dp[i-1] + 1
        if i % 2 == 0: dp[i] = min(dp[i], dp[i//2] + 1)
        if i % 3 == 0: dp[i] = min(dp[i], dp[i//3] + 1)
        if i % 5 == 0: dp[i] = min(dp[i], dp[i//5] + 1)
    return dp[n]
```

* 복잡도 **O(n)**, 공간 **O(n)** (경우에 따라 **O(1)** 압축 가능)

### 3) 0-1 Knapsack(공간 최적화)

```python
def knapsack(wv, W):
    # wv: [(w, v), ...]
    dp = [0]*(W+1)
    for w, v in wv:
        for cap in range(W, w-1, -1):
            dp[cap] = max(dp[cap], dp[cap-w] + v)
    return dp[W]
```

* 복잡도 **O(nW)**, 공간 **O(W)**

### 4) LIS O(n log n)

```python
from bisect import bisect_left

def lis_len(a):
    tails = []
    for x in a:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

## 실전 팁

* **상태정의 → 전이식 → 초깃값 → 답 매핑** 순서로 표를 먼저 설계.
* 메모리 폭발 방지를 위해 **차원/순회 방향(역순 갱신 등)**으로 공간 축소.

---

# 최단 경로 (Shortest Path)

## 개념과 선택 가이드

* 간선 가중치가 **동일/1**: **BFS**
* 가중치가 **비음수**: **Dijkstra(힙)**
* **음수 간선 가능**: **Bellman–Ford**(음수사이클 검출)
* **모든 쌍 최단경로**: **Floyd–Warshall**

## 파이썬 패턴

### 1) Dijkstra (인접 리스트 + 최소 힙)

```python
import heapq

def dijkstra(n, adj, src):
    # adj[u] = [(v, w), ...], 0 <= u < n
    INF = 10**18
    dist = [INF]*n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist
```

* 복잡도: **O(E log V)**

### 2) Bellman–Ford (음수 간선/사이클)

```python
def bellman_ford(n, edges, src):
    INF = 10**18
    dist = [INF]*n
    dist[src] = 0
    for _ in range(n-1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    # 음수사이클 체크
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None  # negative cycle reachable
    return dist
```

* 복잡도: **O(VE)**

### 3) Floyd–Warshall (모든 쌍)

```python
def floyd_warshall(dist):
    # dist[i][j] 초기화 완료(없으면 INF), i==j=0
    n = len(dist)
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            for j in range(n):
                if dik + dk[j] < dist[i][j]:
                    dist[i][j] = dik + dk[j]
    return dist
```

* 복잡도: **O(V^3)**, 공간 **O(V^2)**

## 실전 팁

* Dijkstra에서 **음수 가중치**가 하나라도 있으면 오답.
* 경로 복원: `parent` 배열 유지 후 역추적.
* 그리드 최단경로(가중치 1)는 **BFS**, 가중치 0/1은 **0-1 BFS(deque)** 사용.

---

# 그래프 이론 (Graph Theory)

## 대표 주제와 선택 기준

* 그래프 표현: 인접 리스트(희소), 인접 행렬(밀집)
* MST: Kruskal(간선 정렬 + DSU), Prim(힙)
* 위상정렬: DAG에서 선행관계 순서
* SCC: Kosaraju/Tarjan
* 이분 그래프 판정: BFS 색칠
* 브리지/단절점: DFS 타임스탬프

## 파이썬 패턴

### 1) DSU(Union-Find) — Kruskal용

```python
class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0]*n
    def find(self, x):
        while x != self.p[x]:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1
        return True

def kruskal(n, edges):
    # edges: (w,u,v)
    dsu = DSU(n)
    total = 0
    for w, u, v in sorted(edges):
        if dsu.union(u, v):
            total += w
    return total
```

* 복잡도: 간선 정렬 **O(E log E)**, DSU 연산은 거의 상수(α(n)).

### 2) Prim (힙)

```python
import heapq

def prim(n, adj):
    # adj[u] = [(w, v)]
    used = [False]*n
    pq = [(0, 0)]
    total, taken = 0, 0
    while pq and taken < n:
        w, u = heapq.heappop(pq)
        if used[u]:
            continue
        used[u] = True
        total += w
        taken += 1
        for nw, v in adj[u]:
            if not used[v]:
                heapq.heappush(pq, (nw, v))
    return total
```

* 복잡도: **O(E log V)**

### 3) 위상정렬(Kahn)

```python
from collections import deque

def topo_order(n, adj):
    indeg = [0]*n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    dq = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    while dq:
        u = dq.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                dq.append(v)
    return order  # 사이클 있으면 길이 < n
```

* 복잡도: **O(V+E)**

### 4) 이분 그래프 판정

```python
from collections import deque

def is_bipartite(n, adj):
    color = [0]*n
    for s in range(n):
        if color[s]:
            continue
        color[s] = 1
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for v in adj[u]:
                if color[v] == 0:
                    color[v] = -color[u]
                    dq.append(v)
                elif color[v] == color[u]:
                    return False
    return True
```

## 실전 팁

* 방향 그래프에서 위상정렬은 **선행 제약** 모델링에 매우 유용.
* DSU는 **경로 압축 + 랭크**가 사실상 필수(상수배 성능 향상).
* SCC/브리지/단절점은 **DFS 진입/저점(low-link)** 타임스탬프가 핵심.

---

## 추가 메모 (공통)

* 시간 복잡도 표기는 **입력의 형식**에 민감합니다(그래프는 `V, E` 기준, 격자는 `H, W` 기준).
* 파이썬 실전 유틸:

  * 대용량 입력: `sys.stdin.readline`
  * 큐: `collections.deque` (list `pop(0)` 금지)
  * 우선순위: `heapq`
  * 정렬/이진탐색: `list.sort()/sorted()`, `bisect`
  * 메모이제이션: `functools.lru_cache`
  * 재귀 제한: `sys.setrecursionlimit`
* 알고리즘 선택 순서(경험칙):

  1. 정렬/그리디로 풀리나?
  2. 탐색(DFS/BFS) + 그래프 모델이 맞나?
  3. 단조성이 있어 **이진 탐색(매개변수 탐색)**이 가능한가?
  4. 중복 부분문제가 있어 **DP**가 맞나?
  5. 가중 그래프 최단경로인가(Dijkstra/Bellman-Ford/Floyd)?
  6. 전역 제약(MST/위상/매칭/흐름 등)인가?
