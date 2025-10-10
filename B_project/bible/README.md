# BOJ Bible - Competitive Programming Library

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

백준 온라인 저지(BOJ) 및 프로그래밍 대회를 위한 **완전한 Python 자료구조/알고리즘 라이브러리**입니다.

## 🚀 빠른 시작

### 설치

```bash
# pip 설치 (추후 PyPI 등록 예정)
pip install boj-bible

# 또는 소스에서 설치
git clone https://github.com/yourusername/boj-bible.git
cd boj-bible
pip install -e .
```

### 기본 사용법

```python
# 모듈화된 import
from boj_bible import *
from boj_bible.utils import read_int, read_ints, INF

# 또는 필요한 것만 import
from boj_bible.tree import SegTreeSum
from boj_bible.graph import dijkstra, build_graph

# 세그먼트 트리 사용 예시
st = SegTreeSum([1, 2, 3, 4, 5])
print(st.query(0, 2))  # [0,2] 구간합: 6
```

## 📋 라이브러리 구조

### 🏗️ 모듈 구성

```
boj_bible/
├── basic/          # 기초 자료구조
│   ├── stack_queue.py      # 스택, 큐, 단조스택/큐
│   ├── linked_list.py      # 연결리스트
│   └── union_find.py       # Union-Find (DSU)
├── graph/          # 그래프 알고리즘
│   ├── bfs_dfs.py         # BFS, DFS, 연결요소
│   ├── shortest_path.py   # Dijkstra, Floyd-Warshall
│   └── topological_sort.py # 위상정렬, 사이클 검출
├── tree/           # 트리 자료구조
│   ├── segment_tree.py    # 세그먼트 트리, 펜윅 트리
│   └── lca.py            # LCA, 트리 지름/중심
├── string/         # 문자열 알고리즘
│   ├── pattern_matching.py # KMP, Z-algorithm, Manacher
│   └── trie.py           # 트라이, 바이너리 트라이
├── advanced/       # 고급 알고리즘
│   └── network_flow.py   # 네트워크 플로우
└── utils/          # 유틸리티
    └── fast_io.py        # 빠른 입출력, 상수
```

## 📚 사용법 가이드

### 기초 자료구조

#### 1. 스택과 큐 (basic.stack_queue)

```python
from boj_bible.basic import Stack, Queue, next_greater_indices, sliding_window_min

# 스택 사용법
stack = Stack()
stack.push(1)
stack.push(2)
print(stack.pop())  # 2

# 다음 큰 원소 찾기 (BOJ 17298)
arr = [3, 5, 2, 7]
result = next_greater_indices(arr)  # [1, 3, 3, -1]

# 슬라이딩 윈도우 최솟값
arr = [1, 3, -1, -3, 5, 3, 6, 7]
result = sliding_window_min(arr, 3)  # [-1, -3, -3, -3, 3, 3]
```

#### 02. Linked List
완전한 연결리스트 구현
- 삽입: `append()`, `appendleft()`, `insert(idx, data)`
- 삭제: `pop()`, `popleft()`, `remove(target)`
- 유틸: `reverse()`, `__contains__`, `__len__`

#### 03. HashMap/Set 패턴
- **빈도 카운트**: `Counter` 또는 `defaultdict(int)`
- **멤버십 체크**: `set` 활용

### 중급 자료구조 (04-10)

#### 04. Disjoint Set Union (Union-Find)
```python
dsu = DSU(n)
dsu.union(a, b)     # 연결
dsu.find(x)         # 루트 찾기
```

#### 05. Graph Builder + BFS/DFS
```python
# 그래프 생성 (1-indexed)
edges = [(1,2), (2,3), (1,3)]
g = build_graph(n, edges, directed=False)

# BFS 최단거리
dist = bfs_graph(n, g, start=1)

# 격자 BFS (4방향)
grid = ["...", ".#.", "..."]
dist = bfs_grid(grid, 0, 0)  # 시작점 (0,0)
```

#### 06. Dijkstra / 0-1 BFS / Topological Sort
```python
# Dijkstra: g[u] = [(v, weight), ...]
dist = dijkstra(n, g, start=1)

# 위상정렬
order = topo_sort(n, g, indegree)
```

#### 07. Prefix Sum & Difference Array
```python
# 1D 구간합
ps = prefix_sum_1d([1,2,3,4])  # [0,1,3,6,10]
sum_1_to_3 = ps[4] - ps[1]     # a[1:4] 합

# 2D 구간합
grid = [[1,2], [3,4]]
ps2d = prefix_sum_2d(grid)

# 차분 배열 (구간 덧셈)
diff = Diff1D(n)
diff.range_add(l, r, val)
result = diff.materialize()
```

#### 08. Two Pointers / Sliding Window
```python
# 정렬된 배열에서 합이 X인 쌍
count = two_sum_count_sorted(arr, X)

# 슬라이딩 윈도우 (조건 제한)
max_len = longest_subarray_with_limit(arr, limit)
```

#### 09. Binary Search
```python
# 값 탐색
idx = bisect_left(arr, x)    # lower_bound
idx = bisect_right(arr, x)   # upper_bound

# 파라메트릭 서치 (최댓값)
def ok(mid):
    # 조건 체크
    return True

answer = parametric_max(lo, hi, ok)
```

#### 10. Segment Tree & Fenwick Tree
```python
# 세그먼트 트리 (합)
st = SegTreeSum([1,2,3,4])
st.update(2, 10)        # a[2] = 10
sum_val = st.query(0, 3)  # [0,3] 구간합

# 세그먼트 트리 (최솟값)
st_min = SegTreeMin([5,2,8,1])
min_val = st_min.query(1, 3)

# 펜윅 트리 (1-indexed)
bit = Fenwick(n)
bit.add(i, delta)       # a[i] += delta
sum_val = bit.sum(i)    # a[1:i+1] 합
```

### 고급 알고리즘 (11-29)

#### 11. 문자열: KMP / Trie
```python
# KMP 패턴 매칭
positions = kmp_search(text, pattern)

# 트라이 (접두사 트리)
trie = Trie()
trie.insert("hello")
found = trie.search("hello")    # True
has_prefix = trie.starts_with("hel")  # True
```

#### 12. LIS (Longest Increasing Subsequence)
```python
# O(n log n) LIS 길이
length = lis_length([1,3,2,4,5])  # 4
```

#### 13. MST (Minimum Spanning Tree)
```python
# 크루스칼 알고리즘
edges = [(u, v, weight), ...]
total_weight = kruskal_mst_uv(n, edges)
```

#### 14. Line Sweep (라인 스위핑)
```python
# 구간 병합
intervals = [(1,3), (2,6), (8,10)]
merged = merge_intervals(intervals)  # [(1,6), (8,10)]

# 최대 동시 사용량
events = [(1,1), (2,1), (3,-1), (4,-1)]  # 시작/끝 이벤트
max_concurrent_usage = max_concurrent(events)
```

#### 15. Lazy Propagation Segment Tree
```python
# 구간 덧셈 + 구간 합
st = SegTreeRangeAddSum([1,2,3,4])
st.range_add(1, 3, 5)   # a[1:4]에 모두 +5
sum_val = st.range_sum(0, 3)  # [0,3] 구간합
```

#### 16. Dual Heap (이중 우선순위 큐)
```python
# BOJ 7662용 (최댓값/최솟값 동시 지원)
dh = DualHeap()
dh.push(x)
min_val = dh.pop_min()
max_val = dh.pop_max()
```

#### 17-18. 그래프 심화
```python
# 플로이드-워셜 (모든 쌍 최단거리)
dist, next_matrix = floyd_warshall(adj_matrix)
path = reconstruct_path(u, v, next_matrix)

# LCA (최소 공통 조상)
lca_solver = LCA(n, tree, root=1)
ancestor = lca_solver.lca(u, v)
distance = lca_solver.dist(u, v)

# 트리 지름
u, v, diameter = tree_diameter(n, weighted_tree)
```

#### 19. DP 고급
```python
# 0-1 배낭
max_value = knapsack_01(weights, values, capacity)

# LCS (복원 포함)
length, lcs_string = lcs_restore(str1, str2)

# 히스토그램 최대 직사각형
max_area = largest_rectangle(heights)
```

#### 20-21. 기하 & 좌표압축
```python
# 좌표압축
compressed, unique_vals = compress([100, 5, 100, 200])

# CCW (반시계 방향 판정)
direction = ccw(point_a, point_b, point_c)  # 1:ccw, -1:cw, 0:collinear

# 볼록껍질 (Andrew 알고리즘)
hull_points = convex_hull(points)
```

#### 22. Sparse Table (정적 RMQ)
```python
# O(1) 구간 최솟값 질의
st = SparseTableMin([3,1,4,1,5])
min_val = st.query(1, 3)  # O(1)

# GCD 질의
st_gcd = SparseTableGCD([12,18,24])
gcd_val = st_gcd.query(0, 2)
```

#### 23. SCC & 2-SAT
```python
# 강결합요소 (Tarjan)
scc_solver = TarjanSCC(n)
scc_solver.add_edge(u, v)
comp_count, comp_id = scc_solver.scc()

# 2-SAT
twosat = TwoSAT(n)  # n개 변수
twosat.add_or(0, True, 1, False)  # x0 OR !x1
solution = twosat.solve()  # None 또는 [bool] 리스트
```

#### 24. Aho-Corasick (다중 패턴 매칭)
```python
# 여러 패턴 동시 검색
ac = AhoCorasick()
patterns = ["he", "she", "his", "hers"]
for i, pattern in enumerate(patterns):
    ac.add(pattern, i)
ac.build()

# 텍스트에서 모든 패턴 찾기
matches = ac.search("she sells seashells")  # [(2,1), ...]
```

#### 25. Network Flow
```python
# Dinic (최대 유량)
mf = Dinic(n)
mf.add_edge(u, v, capacity)
max_flow_val = mf.max_flow(source, sink)

# Min-Cost Max-Flow
mcmf = MCMF(n)
mcmf.add_edge(u, v, capacity, cost)
flow, total_cost = mcmf.min_cost_max_flow(source, sink)
```

#### 26-29. 최고급 자료구조
```python
# Mo's Algorithm (오프라인 쿼리)
mo = Mo(array)
queries = [(l1,r1), (l2,r2), ...]
answers = mo.solve(queries)

# Lazy Segment Tree (구간 치환 + RMQ)
st = SegTreeAssignMin([1,2,3,4])
st.range_assign(1, 3, 10)  # [1,3] 구간을 모두 10으로
min_val = st.range_min(0, 3)

# Heavy-Light Decomposition (트리 경로 쿼리)
hld = HLD(n, tree, root=1)
hld.build(node_values)
path_sum = hld.path_sum(u, v)   # u-v 경로 합
path_min = hld.path_min(u, v)   # u-v 경로 최솟값
hld.update_point(node, new_val)
```

## ⚡ 성능 팁

### 시간복잡도 요약
- **세그먼트 트리**: 구축 O(n), 쿼리/수정 O(log n)
- **Fenwick Tree**: O(log n) 수정/쿼리
- **Sparse Table**: 구축 O(n log n), 쿼리 O(1)
- **LIS**: O(n log n)
- **Dijkstra**: O((V+E) log V)
- **KMP**: O(n+m)
- **2-SAT**: O(V+E)

### 메모리 최적화
- **Fenwick Tree** < **Segment Tree** (메모리 사용량)
- **0-1 BFS** < **Dijkstra** (가중치 0/1일 때)
- **Sparse Table** vs **Segment Tree**: 정적 vs 동적 데이터

## 🔧 사용 패턴

### 전형적인 문제 유형별 추천
- **구간합/최솟값**: Segment Tree, Fenwick Tree, Sparse Table
- **그래프 최단거리**: BFS(무가중치), Dijkstra, Floyd-Warshall
- **문자열 매칭**: KMP, Aho-Corasick, Z-Algorithm
- **연결성 판단**: DSU, DFS
- **트리 쿼리**: LCA, HLD
- **기하 문제**: CCW, 볼록껍질
- **조합 최적화**: 2-SAT, Network Flow

### 구현 시 주의사항
1. **인덱싱**: 0-indexed vs 1-indexed 확인
2. **경계 조건**: 빈 배열, 범위 초과 체크
3. **오버플로**: `INF = 10**18` 사용
4. **재귀 제한**: `sys.setrecursionlimit()` 설정

## 📚 학습 순서 추천

### 초보자
1. Stack, Queue, Deque (01)
2. BFS/DFS (05)
3. Binary Search (09)
4. Prefix Sum (07)

### 중급자
1. Segment Tree (10)
2. DSU (04)
3. Dijkstra (06)
4. KMP (11)

### 고급자
1. Heavy-Light Decomposition (27)
2. Network Flow (25, 29)
3. 2-SAT (17, 23, 28)
4. Aho-Corasick (18, 24, 26)

이 라이브러리는 실전 대회와 BOJ에서 바로 사용할 수 있도록 최적화되어 있습니다. 필요한 알고리즘을 복사하여 문제에 맞게 활용하세요!