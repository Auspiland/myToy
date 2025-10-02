# -*- coding: utf-8 -*-
"""
BOJ DS/Algo Bible (Python)
- 빈출 자료구조/알고리즘 기본 틀 모음
- 복붙 후 바로 사용 가능하도록 최소한의 의존성으로 구성
- Python 3.9+

섹션 목차
00. Fast I/O / 유틸
01. Stack / Queue / Deque / Monotonic Stack-Queue
03. Linked list
03. HashMap/Set 패턴 (defaultdict/Counter)
04. Disjoint Set Union (Union-Find)
05. Graph Builder + BFS/DFS (그래프/격자/멀티소스/상태)
06. Dijkstra / 0-1 BFS / Topological Sort
07. Prefix Sum (1D/2D) & Difference Array
08. Two Pointers / Sliding Window 템플릿
09. Binary Search (값/파라메트릭)
10. Segment Tree (Sum/Min) & Fenwick Tree(BIT)
11. 문자열: KMP / Trie
12. 수열: LIS (O(N log N))
13. MST: Kruskal (with DSU)
14. Line Sweep (구간 병합/이벤트)
15. 좌표압축 / 정수 입력 유틸
16. Sparse Table (RMQ: Min/GCD 템플릿)
17. SCC (Tarjan) & 2-SAT Solver
18. Aho–Corasick (다중 패턴 검색)
19. Dinic (Maximum Flow)
20. Min-Cost Max-Flow (SPFA 기반)
21. 기하 기본: CCW / 선분 교차 / 볼록껍질(Andrew)
22. 행렬 거듭제곱 & 모듈러 조합 (nCr mod p)
23. Mo's Algorithm (오프라인 질의 스켈레톤)
24. 세그트리 Lazy (구간 치환 assign / 구간 최솟값 RMQ)
25. LCA + 거리가중 트리: 거리/경로 복원 유틸
26. 문자열: Aho–Corasick(요약) + Z-Algorithm
27. Sparse Table(RMQ) + Heavy-Light Decomposition(경로 쿼리: 합/최솟값)
28. SCC(강결합요소: Kosaraju) + 2-SAT(간단 구현)
29. 네트워크 플로우: Dinic(요약) + Edmonds–Karp

각 섹션은 최소 기능만 담았고, 주석으로 사용 예시를 간단히 명시합니다.
"""

# =============================================================================
# 00. Fast I/O / 유틸
# =============================================================================
import sys, math
from collections import deque, defaultdict, Counter
import heapq
from bisect import bisect_left, bisect_right
from typing import List, Tuple, Dict, Set, Optional, Iterable

input = sys.stdin.readline
INF = 10 ** 18

# =============================================================================
# 01. Stack / Queue / Deque / Monotonic Stack-Queue
# =============================================================================

# Stack: list 사용 (append/pop)
class Stack:
    def __init__(self):
        self._s = []
    def push(self, x):
        self._s.append(x)
    def pop(self):
        return self._s.pop()
    def top(self):
        return self._s[-1]
    def empty(self):
        return not self._s

# Queue: deque 사용 (append/popleft)
class Queue:
    def __init__(self):
        self._q = deque()
    def push(self, x):
        self._q.append(x)
    def pop(self):
        return self._q.popleft()
    def empty(self):
        return not self._q

# Deque: collections.deque 그대로 사용 권장
# 예) dq = deque(); dq.append(x); dq.appendleft(x); dq.pop(); dq.popleft()

# Monotonic Stack: 다음 큰 원소(Next Greater Element) 예시 - 최적화됨
# arr의 각 i에 대해 오른쪽에서 처음으로 자신보다 큰 값의 인덱스를 구함 (없으면 -1)
def next_greater_indices(arr: List[int]) -> List[int]:
    n = len(arr)
    ans = [-1] * n
    st = []  # 값이 감소하는 단조 스택: top이 가장 작게 유지
    for i in range(n):
        while st and arr[st[-1]] < arr[i]:
            ans[st.pop()] = i
        st.append(i)
    return ans

# Monotonic Queue: 슬라이딩 윈도우 최소값 (deque에 인덱스를 저장) - 최적화됨
def sliding_window_min(arr: List[int], k: int) -> List[int]:
    if not arr or k <= 0:
        return []
    n = len(arr)
    dq = deque()  # 증가 단조: front가 최소값 인덱스
    res = []
    for i in range(n):
        # 범위 밖 제거
        while dq and dq[0] <= i - k:
            dq.popleft()
        # 단조성 유지
        while dq and arr[dq[-1]] >= arr[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            res.append(arr[dq[0]])
    return res

# =============================================================================
# 02. Linked List
# =============================================================================
class LNode():
    def __init__(self, _data, _next = None):
        self.data = _data
        self.next = _next


class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def __len__(self):
        return self.length

    def appendleft(self, data):
        if self.head is None:
            self.head = LNode(data)
        else:
            self.head = LNode(data, self.head)
        self.length += 1

    def append(self, data):
        if self.head is None:
            self.head = LNode(data)
        else:
            node = self.head
            while node.next is not None:
                node = node.next
            node.next = LNode(data)
        self.length += 1

    def __str__(self):
        res = "Head"
        if self.head is None:
            return f"{res} → None"
        node = self.head
        while node is not None:
            res = f"{res} → {str(node.data)}"
            node = node.next
        return res

    def __contains__(self, target):
        if self.head is None:
            return False
        node = self.head
        while node is not None:
            if node.data == target:
                return True
            node = node.next
        return False

    def popleft(self):
        if self.head is None:
            return None
        node = self.head
        self.head = self.head.next
        self.length -= 1
        return node.data

    def pop(self):
        if self.head is None:
            return None
        prev = None
        node = self.head
        while node.next is not None:
            prev = node
            node = node.next
        if prev is None:
            self.head = None
        else:
            prev.next = None
        self.length -= 1
        return node.data

    def remove(self, target):
        node = self.head
        while node is not None and node.data != target:
            prev = node
            node = node.next
        if node is None:
            return False
        if node == self.head:
            self.head = self.head.next
        else:
            prev.next = node.next
        self.length -= 1
        return True

    def insert(self, idx, data):
        if idx <= 0:
            self.appendleft(data)
        elif idx >= self.length:
            self.append(data)
        else:
            node = self.head
            for _ in range(idx - 1):
                node = node.next
            new_node = LNode(data, node.next)
            node.next = new_node
            self.length += 1

    def reverse(self):
        if self.length < 2:
            return
        prev = None
        ahead = self.head.next
        while ahead:
            self.head.next = prev
            prev = self.head
            self.head = ahead
            ahead = ahead.next
        self.head.next = prev

# =============================================================================
# 03. HashMap/Set 패턴 (defaultdict/Counter)
# =============================================================================

# 빈도 카운트: Counter 또는 defaultdict(int)
def freq_count(arr: List[int]) -> Dict[int, int]:
    # return Counter(arr)
    d = defaultdict(int)
    for x in arr:
        d[x] += 1
    return d

# 멤버십 체크: set
# s = set(arr); if x in s: ...

# =============================================================================
# 04. Disjoint Set Union (Union-Find)
# =============================================================================
class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
    def find(self, x: int) -> int:
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

# =============================================================================
# 05. Graph Builder + BFS/DFS (그래프/격자/멀티소스/상태)
# =============================================================================

# 인접 리스트 그래프 생성 (1-indexed 예시)
def build_graph(n: int, edges: List[Tuple[int, int]], directed: bool = False) -> List[List[int]]:
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
        if not directed:
            g[v].append(u)
    return g

# BFS (무가중치 최단거리)
def bfs_graph(n: int, g: List[List[int]], start: int) -> List[int]:
    dist = [-1] * (n + 1)
    q = deque([start])
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

# DFS (반복형)
def dfs_graph(n: int, g: List[List[int]], start: int) -> List[int]:
    order = []
    st = [start]
    visited = [False] * (n + 1)
    visited[start] = True
    while st:
        u = st.pop()
        order.append(u)
        for v in g[u]:
            if not visited[v]:
                visited[v] = True
                st.append(v)
    return order

# 격자 BFS (4방향)
def bfs_grid(grid: List[str], sx: int, sy: int) -> List[List[int]]:
    n, m = len(grid), len(grid[0])
    dist = [[-1] * m for _ in range(n)]
    q = deque([(sx, sy)])
    dist[sx][sy] = 0
    for x, y in q:
        pass  # just to use tuple unpacking type hints
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and dist[nx][ny] == -1 and grid[nx][ny] != '#':
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    return dist

# 멀티소스 BFS (여러 시작점)
def multi_source_bfs(starts: List[Tuple[int, int]], grid: List[str]) -> List[List[int]]:
    n, m = len(grid), len(grid[0])
    dist = [[-1] * m for _ in range(n)]
    q = deque()
    for x, y in starts:
        dist[x][y] = 0
        q.append((x, y))
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and dist[nx][ny] == -1 and grid[nx][ny] != '#':
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    return dist

# 상태 BFS 예시: (x, y, used) 처럼 추가 상태 차원을 가질 때
# visited를 dict/set 또는 3D 배열로 관리
from typing import NamedTuple
class State(NamedTuple):
    x: int
    y: int
    used: int  # 예: 벽을 부순 여부(0/1)

def bfs_state(grid: List[str], sx: int, sy: int) -> int:
    n, m = len(grid), len(grid[0])
    visited = [[[False]*2 for _ in range(m)] for __ in range(n)]
    q = deque()
    q.append((sx, sy, 0, 0))  # x, y, used, dist
    visited[sx][sy][0] = True
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    while q:
        x, y, used, d = q.popleft()
        if (x, y) == (n-1, m-1):
            return d
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                w = grid[nx][ny]
                if w != '#' and not visited[nx][ny][used]:
                    visited[nx][ny][used] = True
                    q.append((nx, ny, used, d+1))
                # 예: 벽('#')을 한번 부술 수 있는 경우
                if w == '#' and used == 0 and not visited[nx][ny][1]:
                    visited[nx][ny][1] = True
                    q.append((nx, ny, 1, d+1))
    return -1

# =============================================================================
# 06. Dijkstra / 0-1 BFS / Topological Sort
# =============================================================================

# Dijkstra: 인접 리스트, 양의 가중치 - 최적화됨
# g[u] = [(v, w), ...]
def dijkstra(n: int, g: List[List[Tuple[int, int]]], start: int) -> List[int]:
    dist = [INF] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:  # 조건 최적화
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

# 0-1 BFS: 간선 가중치가 0 또는 1일 때
# g[u] = [(v, w in {0,1})]
def zero_one_bfs(n: int, g: List[List[Tuple[int, int]]], start: int) -> List[int]:
    dist = [INF] * (n + 1)
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v, w in g[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist

# Topological Sort (Kahn)
# 입력: n, g(인접리스트), indeg(각 노드 진입차수)
def topo_sort(n: int, g: List[List[int]], indeg: List[int]) -> List[int]:
    q = deque([i for i in range(1, n+1) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order  # DAG가 아니면 일부만 반환

# =============================================================================
# 07. Prefix Sum (1D/2D) & Difference Array
# =============================================================================

# 1D Prefix Sum
# ps[i] = a[0..i-1] 합, 길이 n+1
# 구간합 a[l..r] = ps[r+1] - ps[l]
def prefix_sum_1d(a: List[int]) -> List[int]:
    n = len(a)
    ps = [0] * (n + 1)
    for i in range(n):
        ps[i+1] = ps[i] + a[i]
    return ps

# 2D Prefix Sum: grid는 int 2D
# sum of rect (x1..x2, y1..y2) inclusive
# s[x+1][y+1] = grid[x][y] + s[x][y+1] + s[x+1][y] - s[x][y]
def prefix_sum_2d(grid: List[List[int]]) -> List[List[int]]:
    n, m = len(grid), len(grid[0])
    s = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n):
        row_sum = 0
        for j in range(m):
            row_sum += grid[i][j]
            s[i+1][j+1] = s[i][j+1] + row_sum
    return s

# Difference Array (range add, point query) 예시
class Diff1D:
    def __init__(self, n: int):
        self.d = [0]*(n+1)
    def range_add(self, l: int, r: int, val: int):
        self.d[l] += val
        if r+1 < len(self.d):
            self.d[r+1] -= val
    def materialize(self) -> List[int]:
        res = [0]*(len(self.d)-1)
        cur = 0
        for i in range(len(res)):
            cur += self.d[i]
            res[i] = cur
        return res

# =============================================================================
# 08. Two Pointers / Sliding Window 템플릿
# =============================================================================

# 정렬된 배열에서 합이 X인 쌍의 개수
def two_sum_count_sorted(a: List[int], X: int) -> int:
    a.sort()
    i, j, cnt = 0, len(a)-1, 0
    while i < j:
        s = a[i] + a[j]
        if s == X:
            cnt += 1
            i += 1
            j -= 1
        elif s < X:
            i += 1
        else:
            j -= 1
    return cnt

# 문자 빈도 제약 슬라이딩 윈도우 예시 - 최적화됨
def longest_subarray_with_limit(a: List[int], limit: int) -> int:
    if not a or limit < 0:
        return 0
    maxdq, mindq = deque(), deque()  # 인덱스를 저장
    ans = 0
    l = 0
    for r in range(len(a)):
        val = a[r]
        # 단조성 유지 - 최적화
        while maxdq and a[maxdq[-1]] <= val:
            maxdq.pop()
        while mindq and a[mindq[-1]] >= val:
            mindq.pop()
        maxdq.append(r)
        mindq.append(r)
        # 윈도우 조건 최적화
        while maxdq and mindq and a[maxdq[0]] - a[mindq[0]] > limit:
            l += 1
            if maxdq and maxdq[0] < l:
                maxdq.popleft()
            if mindq and mindq[0] < l:
                mindq.popleft()
        ans = max(ans, r - l + 1)
    return ans

# =============================================================================
# 09. Binary Search (값/파라메트릭)
# =============================================================================

# 값 탐색: bisect 활용
def lower_bound(a: List[int], x: int) -> int:
    return bisect_left(a, x)

def upper_bound(a: List[int], x: int) -> int:
    return bisect_right(a, x)

# 파라메트릭 서치 (최댓값 예시)
# ok(mid) 가 True면 더 크게, False면 줄이는 패턴
# 경계/단조성 주의

def parametric_max(lo: int, hi: int, ok) -> int:
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo

# =============================================================================
# 10. Segment Tree (Sum/Min) & Fenwick Tree(BIT)
# =============================================================================

class SegTreeSum:
    """Segment Tree for Sum queries - Optimized iterative version"""
    __slots__ = ('N', 'seg')
    
    def __init__(self, a: List[int]):
        n = len(a)
        self.N = 1
        while self.N < n:
            self.N <<= 1
        self.seg = [0] * (2 * self.N)
        # build - 최적화된 방식
        for i in range(n):
            self.seg[self.N + i] = a[i]
        for i in range(self.N - 1, 0, -1):
            self.seg[i] = self.seg[i << 1] + self.seg[i << 1 | 1]
    
    def update(self, idx: int, val: int):  # set a[idx] = val
        i = self.N + idx
        self.seg[i] = val
        while i > 1:
            i >>= 1
            self.seg[i] = self.seg[i << 1] + self.seg[i << 1 | 1]
    
    def query(self, l: int, r: int) -> int:  # inclusive l..r
        l += self.N; r += self.N
        res = 0
        while l <= r:
            if l & 1:
                res += self.seg[l]
                l += 1
            if not (r & 1):
                res += self.seg[r]
                r -= 1
            l >>= 1; r >>= 1
        return res

class SegTreeMin:
    """Segment Tree for Min queries - Optimized iterative version"""
    __slots__ = ('N', 'seg')
    
    def __init__(self, a: List[int]):
        n = len(a)
        self.N = 1
        while self.N < n:
            self.N <<= 1
        self.seg = [INF] * (2 * self.N)
        for i in range(n):
            self.seg[self.N + i] = a[i]
        for i in range(self.N - 1, 0, -1):
            self.seg[i] = min(self.seg[i << 1], self.seg[i << 1 | 1])
    
    def update(self, idx: int, val: int):
        i = self.N + idx
        self.seg[i] = val
        while i > 1:
            i >>= 1
            self.seg[i] = min(self.seg[i << 1], self.seg[i << 1 | 1])
    
    def query(self, l: int, r: int) -> int:
        l += self.N; r += self.N
        res = INF
        while l <= r:
            if l & 1:
                res = min(res, self.seg[l])
                l += 1
            if not (r & 1):
                res = min(res, self.seg[r])
                r -= 1
            l >>= 1; r >>= 1
        return res

# Fenwick Tree (BIT): 1-indexed 내부구현 - 최적화됨
class Fenwick:
    """Binary Indexed Tree for prefix sum queries"""
    __slots__ = ('n', 'bit')
    
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)
    
    def add(self, i: int, delta: int):
        """Add delta to a[i] (1-indexed)"""
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i
    
    def sum(self, i: int) -> int:
        """Sum of a[1..i] (1-indexed)"""
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s
    
    def range_sum(self, l: int, r: int) -> int:
        """Sum of a[l..r] (1-indexed)"""
        return self.sum(r) - self.sum(l-1)
    
    def find_kth(self, k: int) -> int:
        """Find k-th element (1-indexed) - O(log n)"""
        pos = 0
        bit_mask = 1
        while bit_mask <= self.n:
            bit_mask <<= 1
        bit_mask >>= 1
        
        while bit_mask > 0:
            if pos + bit_mask <= self.n and self.bit[pos + bit_mask] < k:
                k -= self.bit[pos + bit_mask]
                pos += bit_mask
            bit_mask >>= 1
        return pos + 1

# =============================================================================
# 11. 문자열: KMP / Trie
# =============================================================================

# KMP: 부분 문자열 검색 (패턴 p, 본문 s)

def kmp_lps(p: str) -> List[int]:
    """Compute LPS (Longest Prefix Suffix) array for KMP - Optimized"""
    n = len(p)
    lps = [0] * n
    j = 0
    for i in range(1, n):
        while j and p[i] != p[j]:
            j = lps[j-1]
        if p[i] == p[j]:
            j += 1
        lps[i] = j
    return lps

def kmp_search(s: str, p: str) -> List[int]:
    """KMP string matching - optimized version"""
    if not s or not p:
        return []
    
    lps = kmp_lps(p)
    j = 0
    res = []
    n, m = len(s), len(p)
    
    for i in range(n):
        while j and s[i] != p[j]:
            j = lps[j-1]
        if s[i] == p[j]:
            j += 1
            if j == m:
                res.append(i - j + 1)  # 매칭 시작 인덱스
                j = lps[j-1]
    return res

# Trie (알파벳 소문자 예시)
class TrieNode:
    __slots__ = ("child", "end")
    def __init__(self):
        self.child: Dict[str, TrieNode] = {}
        self.end: bool = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word: str):
        cur = self.root
        for ch in word:
            if ch not in cur.child:
                cur.child[ch] = TrieNode()
            cur = cur.child[ch]
        cur.end = True
    def search(self, word: str) -> bool:
        cur = self.root
        for ch in word:
            if ch not in cur.child:
                return False
            cur = cur.child[ch]
        return cur.end
    def starts_with(self, prefix: str) -> bool:
        cur = self.root
        for ch in prefix:
            if ch not in cur.child:
                return False
            cur = cur.child[ch]
        return True

# =============================================================================
# 12. 수열: LIS (O(N log N))
# =============================================================================

def lis_length(a: List[int]) -> int:
    """Longest Increasing Subsequence length - O(n log n)"""
    if not a:
        return 0
    
    d = []
    for x in a:
        i = bisect_left(d, x)
        if i == len(d):
            d.append(x)
        else:
            d[i] = x
    return len(d)

def lis_with_path(a: List[int]) -> Tuple[int, List[int]]:
    """LIS with path reconstruction - O(n log n)"""
    if not a:
        return 0, []
    
    n = len(a)
    d = []
    parent = [-1] * n
    pos = [-1] * n
    
    for i, x in enumerate(a):
        j = bisect_left(d, x)
        if j == len(d):
            d.append(x)
        else:
            d[j] = x
        pos[i] = j
        if j > 0:
            # Find the previous element
            for k in range(i-1, -1, -1):
                if pos[k] == j-1 and a[k] < x:
                    parent[i] = k
                    break
    
    # Reconstruct path
    lis_len = len(d)
    path = []
    cur = -1
    for i in range(n-1, -1, -1):
        if pos[i] == lis_len - 1:
            cur = i
            break
    
    while cur != -1:
        path.append(a[cur])
        cur = parent[cur]
    
    path.reverse()
    return lis_len, path

# 복원형(인덱스 추적): 필요 시 별도 구현 권장

# =============================================================================
# 13. MST: Kruskal (with DSU)
# =============================================================================

def kruskal_mst(n: int, edges: List[Tuple[int, int, int]]) -> int:
    """
    edges: (w, u, v) 또는 (u, v, w) 상관없이 아래에서 정렬 기준 맞추어 사용
    반환: MST 총 가중치 (연결 불가 시 일부만 연결될 수 있으므로 문제 조건 확인)
    """
    # (w, u, v) 형태로 맞춤
    norm = []
    for e in edges:
        if len(e) != 3:
            raise ValueError("Edge must be (u, v, w) or (w, u, v)")
        a, b, c = e
        if a <= b and b <= c:  # 대충 판별이 모호하므로 명시적으로 재배치 권장
            # 기본 가정: (u, v, w)
            u, v, w = a, b, c
        else:
            # 기본 가정 실패 시 (w, u, v) 형태일 가능성
            w, u, v = a, b, c
        norm.append((w, u, v))
    norm.sort()
    dsu = DSU(n+1)
    total = 0
    for w, u, v in norm:
        if dsu.union(u, v):
            total += w
    return total

# =============================================================================
# 14. Line Sweep (구간 병합/이벤트)
# =============================================================================

# 구간 병합: [l, r] 폐구간들 병합 후 총 길이/구간 반환

def merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not intervals:
        return []
    intervals.sort()
    res = []
    cur_l, cur_r = intervals[0]
    for l, r in intervals[1:]:
        if l <= cur_r:  # overlap
            cur_r = max(cur_r, r)
        else:
            res.append((cur_l, cur_r))
            cur_l, cur_r = l, r
    res.append((cur_l, cur_r))
    return res

# 이벤트 스위핑: 예) 동시 사용량 최대값
# events: (x, +1/-1) 형태, 같은 x에서는 +1 먼저 처리 권장

def max_concurrent(events: List[Tuple[int, int]]) -> int:
    events.sort(key=lambda x: (x[0], -x[1]))
    cur = ans = 0
    for _, delta in events:
        cur += delta
        ans = max(ans, cur)
    return ans

# =============================================================================
# 사용 예시 (주석) (1~15번)
# =============================================================================
# 1) 그래프 최단거리 (무가중치)
# n, m = map(int, input().split())
# edges = [tuple(map(int, input().split())) for _ in range(m)]
# g = build_graph(n, edges)
# dist = bfs_graph(n, g, start=1)
# print(dist[n])
#
# 2) 세그먼트 트리 합
# a = list(map(int, input().split()))
# st = SegTreeSum(a)
# print(st.query(0, len(a)-1))
# st.update(3, 10)
#
# 3) KMP
# s = input().strip(); p = input().strip()
# pos = kmp_search(s, p)
# print(len(pos))
#
# 4) LIS 길이
# n = int(input()); a = list(map(int, input().split()))
# print(lis_length(a))

# =============================================================================
# 15. Segment Tree with Lazy Propagation (Range Add / Range Sum)
# =============================================================================

class SegTreeRangeAddSum:
    """구간 덧셈 + 구간 합 질의 (0-indexed 외부 인터페이스)
    - build O(n), update/query O(log n)
    - 내부는 1-indexed, size=4*n 재귀 구현
    """
    def __init__(self, a: List[int]):
        self.n = len(a)
        self.seg = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        if self.n:
            self._build(1, 0, self.n - 1, a)

    def _build(self, idx: int, l: int, r: int, a: List[int]):
        if l == r:
            self.seg[idx] = a[l]
            return
        m = (l + r) // 2
        self._build(idx*2, l, m, a)
        self._build(idx*2+1, m+1, r, a)
        self.seg[idx] = self.seg[idx*2] + self.seg[idx*2+1]

    def _prop(self, idx: int, l: int, r: int):
        if self.lazy[idx] != 0:
            add = self.lazy[idx]
            self.seg[idx] += add * (r - l + 1)
            if l != r:
                self.lazy[idx*2] += add
                self.lazy[idx*2+1] += add
            self.lazy[idx] = 0

    def _update(self, idx: int, l: int, r: int, ql: int, qr: int, val: int):
        self._prop(idx, l, r)
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            self.lazy[idx] += val
            self._prop(idx, l, r)
            return
        m = (l + r) // 2
        self._update(idx*2, l, m, ql, qr, val)
        self._update(idx*2+1, m+1, r, ql, qr, val)
        self.seg[idx] = self.seg[idx*2] + self.seg[idx*2+1]

    def _query(self, idx: int, l: int, r: int, ql: int, qr: int) -> int:
        self._prop(idx, l, r)
        if qr < l or r < ql:
            return 0
        if ql <= l and r <= qr:
            return self.seg[idx]
        m = (l + r) // 2
        return self._query(idx*2, l, m, ql, qr) + self._query(idx*2+1, m+1, r, ql, qr)

    def range_add(self, l: int, r: int, val: int):
        if l > r: return
        self._update(1, 0, self.n - 1, l, r, val)

    def range_sum(self, l: int, r: int) -> int:
        if l > r: return 0
        return self._query(1, 0, self.n - 1, l, r)


# =============================================================================
# 16. Double-Ended Priority Queue (이중 우선순위 큐, BOJ 7662용)
# =============================================================================

class DualHeap:
    """min-heap / max-heap + lazy 삭제 동기화"""
    def __init__(self):
        self.minh = []
        self.maxh = []
        self.count = defaultdict(int)
        self.live = 0

    def _clean(self, h, sign):
        # sign=+1 for minh, -1 for maxh (because maxh stores -x)
        while h:
            x = h[0] * sign
            if self.count[x] == 0:
                heapq.heappop(h)
            else:
                break

    def push(self, x: int):
        heapq.heappush(self.minh, x)
        heapq.heappush(self.maxh, -x)
        self.count[x] += 1
        self.live += 1

    def pop_min(self) -> Optional[int]:
        if self.live == 0:
            return None
        self._clean(self.minh, +1)
        if not self.minh:
            return None
        x = heapq.heappop(self.minh)
        if self.count[x] > 0:
            self.count[x] -= 1
            self.live -= 1
            # 대응 원소는 lazy 삭제로 남겨두고, 필요 시 _clean에서 제거
            return x
        return None

    def pop_max(self) -> Optional[int]:
        if self.live == 0:
            return None
        self._clean(self.maxh, -1)
        if not self.maxh:
            return None
        x = -heapq.heappop(self.maxh)
        if self.count[x] > 0:
            self.count[x] -= 1
            self.live -= 1
            return x
        return None

    def peek_min(self) -> Optional[int]:
        if self.live == 0:
            return None
        self._clean(self.minh, +1)
        return self.minh[0] if self.minh else None

    def peek_max(self) -> Optional[int]:
        if self.live == 0:
            return None
        self._clean(self.maxh, -1)
        return -self.maxh[0] if self.maxh else None

    def __len__(self):
        return self.live


# =============================================================================
# 17. Floyd–Warshall (All-Pairs Shortest Path) + 경로 복원
# =============================================================================

def floyd_warshall(dist: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
    """입력: dist[i][j] = 간선 가중치(없으면 INF), dist[i][i]=0 권장
    반환: (최단거리행렬, next 행렬)  next[i][j]는 i→j 최단경로에서 i 다음 노드
    """
    n = len(dist)
    nxt = [[-1]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if dist[i][j] < INF:
                nxt[i][j] = j
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            di = dist[i]
            dik = di[k]
            if dik == INF: continue
            for j in range(n):
                alt = dik + dk[j]
                if alt < di[j]:
                    di[j] = alt
                    nxt[i][j] = nxt[i][k]
    return dist, nxt


def reconstruct_path(u: int, v: int, nxt: List[List[int]]) -> List[int]:
    if nxt[u][v] == -1:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path


# =============================================================================
# 18. Tree: Diameter / LCA (Binary Lifting)
# =============================================================================

# 트리 지름 (두 번의 BFS/DFS)

def tree_diameter(n: int, g: List[List[Tuple[int,int]]], start: int = 1) -> Tuple[int,int,int]:
    """가중 트리 지름: g[u] = [(v, w)]  반환: (u, v, dist)
    무가중의 경우 w=1로 주면 됨
    """
    def bfs(src: int):
        dist = [INF]*(n+1)
        dist[src] = 0
        dq = deque([src])
        while dq:
            u = dq.popleft()
            for v, w in g[u]:
                nd = dist[u] + w
                if nd < dist[v]:
                    dist[v] = nd
                    dq.append(v)
        mx = max(range(1, n+1), key=lambda x: dist[x])
        return mx, dist
    a, da = bfs(start)
    b, db = bfs(a)
    return a, b, db[b]


# LCA with Binary Lifting (1-indexed nodes)
class LCA:
    def __init__(self, n: int, g: List[List[int]], root: int = 1):
        self.n = n
        self.LOG = (n).bit_length()
        self.up = [[0]*(n+1) for _ in range(self.LOG)]
        self.depth = [0]*(n+1)
        self._build(g, root)

    def _build(self, g: List[List[int]], root: int):
        q = deque([root])
        self.up[0][root] = 0
        self.depth[root] = 0
        visited = [False]*(self.n+1)
        visited[root] = True
        while q:
            u = q.popleft()
            for v in g[u]:
                if not visited[v]:
                    visited[v] = True
                    self.up[0][v] = u
                    self.depth[v] = self.depth[u] + 1
                    q.append(v)
        for k in range(1, self.LOG):
            upk = self.up[k]
            upk_1 = self.up[k-1]
            for v in range(1, self.n+1):
                upk[v] = upk_1[upk_1[v]]

    def lca(self, a: int, b: int) -> int:
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        # raise a to depth of b
        diff = self.depth[a] - self.depth[b]
        k = 0
        while diff:
            if diff & 1:
                a = self.up[k][a]
            diff >>= 1
            k += 1
        if a == b:
            return a
        for k in range(self.LOG-1, -1, -1):
            if self.up[k][a] != self.up[k][b]:
                a = self.up[k][a]
                b = self.up[k][b]
        return self.up[0][a]

    def dist(self, a: int, b: int) -> int:
        c = self.lca(a, b)
        return self.depth[a] + self.depth[b] - 2*self.depth[c]


# =============================================================================
# 19. DP: 0-1 Knapsack / LCS(복원) / Histogram Max Rectangle
# =============================================================================

# 0-1 Knapsack (1D 최적화)

def knapsack_01(weights: List[int], values: List[int], W: int) -> int:
    dp = [0]*(W+1)
    for w, v in zip(weights, values):
        for cap in range(W, w-1, -1):
            dp[cap] = max(dp[cap], dp[cap-w] + v)
    return dp[W]

# LCS 길이 및 하나의 공통 수열 복원 (문자열)

def lcs_restore(a: str, b: str) -> Tuple[int, str]:
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        ai = a[i-1]
        dpi = dp[i]
        dpim1 = dp[i-1]
        for j in range(1, m+1):
            if ai == b[j-1]:
                dpi[j] = dpim1[j-1] + 1
            else:
                dpi[j] = dpim1[j] if dpim1[j] >= dpi[j-1] else dpi[j-1]
    # 복원
    i, j = n, m
    out = []
    while i > 0 and j > 0:
        if a[i-1] == b[j-1]:
            out.append(a[i-1]); i -= 1; j -= 1
        else:
            if dp[i-1][j] >= dp[i][j-1]:
                i -= 1
            else:
                j -= 1
    out.reverse()
    return dp[n][m], ''.join(out)

# 히스토그램에서 최대 직사각형 (O(n))

def largest_rectangle(heights: List[int]) -> int:
    st = []  # indices, 증가 단조
    ans = 0
    for i, h in enumerate(heights + [0]):  # sentinel
        while st and heights[st[-1]] > h:
            top = st.pop()
            height = heights[top]
            left = st[-1] + 1 if st else 0
            width = i - left
            area = height * width
            if area > ans:
                ans = area
        st.append(i)
    return ans

# =============================================================================
# 20. Kruskal (안전 버전) - (u, v, w) 명시 입력
# =============================================================================

def kruskal_mst_uv(n: int, edges: List[Tuple[int, int, int]]) -> int:
    """edges: (u, v, w) 명시. 1-indexed 노드 가정. 반환: MST 총 가중치.
    그래프가 비연결이면 일부만 선택되니 문제 조건 확인 필요.
    """
    dsu = DSU(n+1)
    total = 0
    for u, v, w in sorted(edges, key=lambda x: x[2]):
        if dsu.union(u, v):
            total += w
    return total

# =============================================================================
# 15. 좌표압축 / 정수 입력 유틸 + 추가 최적화
# =============================================================================

def compress(values: Iterable[int]) -> Tuple[List[int], List[int]]:
    """좌표압축: 원본 values -> [0..K-1] 로 매핑
    반환: (압축된 리스트, 정렬된 고유값 리스트)
    """
    vals = sorted(set(values))
    idx = {v: i for i, v in enumerate(vals)}
    return [idx[v] for v in values], vals

# 빠른 정수 리스트 입력
def read_ints() -> List[int]:
    return list(map(int, input().split()))

# 추가 최적화: 디스크리트 로그 트릭 (Discrete Log Trick)
def discrete_log_trick(a: List[int]) -> List[int]:
    """Convert array to discrete log representation for faster operations"""
    if not a:
        return []
    
    # 정렬된 고유값 생성
    sorted_unique = sorted(set(a))
    val_to_idx = {v: i for i, v in enumerate(sorted_unique)}
    
    return [val_to_idx[x] for x in a]

# 고속 중복 제거
def fast_unique(a: List[int]) -> List[int]:
    """Fast unique preserving order - O(n)"""
    seen = set()
    result = []
    for x in a:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result

# =============================================================================
# 16. Sparse Table (RMQ: Min/GCD 템플릿)
# =============================================================================

class SparseTableMin:
    """정적 배열에 대한 구간 최소 질의 O(1), 전처리 O(n log n)
    query(l, r): inclusive
    """
    def __init__(self, a: List[int]):
        self.n = len(a)
        self.LOG = (self.n).bit_length()
        self.st = [a[:] ]  # k=0
        k = 1
        while (1 << k) <= self.n:
            prev = self.st[k-1]
            size = self.n - (1 << k) + 1
            cur = [0] * size
            half = 1 << (k-1)
            for i in range(size):
                cur[i] = prev[i] if prev[i] <= prev[i + half] else prev[i + half]
            self.st.append(cur)
            k += 1

    def query(self, l: int, r: int) -> int:
        if l > r: l, r = r, l
        k = (r - l + 1).bit_length() - 1
        half = 1 << k
        a = self.st[k][l]
        b = self.st[k][r - half + 1]
        return a if a <= b else b

class SparseTableGCD:
    def __init__(self, a: List[int]):
        self.n = len(a)
        self.LOG = (self.n).bit_length()
        self.st = [a[:] ]
        k = 1
        while (1 << k) <= self.n:
            prev = self.st[k-1]
            size = self.n - (1 << k) + 1
            cur = [0] * size
            half = 1 << (k-1)
            for i in range(size):
                cur[i] = math.gcd(prev[i], prev[i + half])
            self.st.append(cur)
            k += 1
    def query(self, l: int, r: int) -> int:
        if l > r: l, r = r, l
        k = (r - l + 1).bit_length() - 1
        half = 1 << k
        return math.gcd(self.st[k][l], self.st[k][r - half + 1])

# =============================================================================
# 17. SCC (Tarjan) & 2-SAT Solver
# =============================================================================

class TarjanSCC:
    def __init__(self, n: int):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.id = 0
        self.ids = [-1]*n
        self.low = [0]*n
        self.on = [False]*n
        self.st = []
        self.comp_id = [-1]*n
        self.comp_cnt = 0
        sys.setrecursionlimit(1_000_000)

    def add_edge(self, u: int, v: int):
        self.g[u].append(v)

    def _dfs(self, at: int):
        self.ids[at] = self.low[at] = self.id; self.id += 1
        self.st.append(at); self.on[at] = True
        for to in self.g[at]:
            if self.ids[to] == -1:
                self._dfs(to)
                self.low[at] = min(self.low[at], self.low[to])
            elif self.on[to]:
                self.low[at] = min(self.low[at], self.ids[to])
        if self.ids[at] == self.low[at]:
            while True:
                node = self.st.pop(); self.on[node] = False
                self.comp_id[node] = self.comp_cnt
                if node == at:
                    break
            self.comp_cnt += 1

    def scc(self) -> Tuple[int, List[int]]:
        for i in range(self.n):
            if self.ids[i] == -1:
                self._dfs(i)
        return self.comp_cnt, self.comp_id

class TwoSAT:
    """변수 x in [0..n-1]
    노드 매핑: x_false=2*x, x_true=2*x^1
    add_or(a, aval, b, bval): (x_a==aval) or (x_b==bval)
    """
    def __init__(self, n: int):
        self.n = n
        self.tg = TarjanSCC(2*n)

    @staticmethod
    def _id(x: int, val: bool) -> int:
        return 2*x ^ (1 if val else 0)

    def add_imp(self, u: int, v: int):
        self.tg.add_edge(u, v)

    def add_or(self, a: int, aval: bool, b: int, bval: bool):
        u = self._id(a, not aval)
        v = self._id(b, bval)
        self.add_imp(u, v)
        u2 = self._id(b, not bval)
        v2 = self._id(a, aval)
        self.add_imp(u2, v2)

    def add_true(self, a: int, aval: bool):
        # (x_a == aval)
        self.add_imp(self._id(a, not aval), self._id(a, aval))

    def add_equal(self, a: int, b: int):
        # a == b
        self.add_or(a, True, b, False)
        self.add_or(a, False, b, True)

    def add_xor(self, a: int, b: int):
        # a XOR b
        self.add_or(a, True, b, True)
        self.add_or(a, False, b, False)

    def solve(self) -> Optional[List[bool]]:
        _, comp = self.tg.scc()
        assign = [False]*self.n
        for x in range(self.n):
            if comp[2*x] == comp[2*x^1]:
                return None
        order = sorted(range(2*self.n), key=lambda i: comp[i])
        val = [False]*(2*self.n)
        for v in order:
            neg = v^1
            if not val[v] and not val[neg]:
                val[v] = True
        for x in range(self.n):
            assign[x] = val[2*x^1]
        return assign

# =============================================================================
# 18. Aho–Corasick (다중 패턴 검색)
# =============================================================================

class ACNode:
    __slots__ = ("nxt", "fail", "out")
    def __init__(self):
        self.nxt: Dict[str, int] = {}
        self.fail: int = 0
        self.out: List[int] = []  # 매칭된 패턴 인덱스 목록

class AhoCorasick:
    def __init__(self):
        self.trie = [ACNode()]  # 0: root

    def add(self, word: str, idx: int):
        node = 0
        for ch in word:
            if ch not in self.trie[node].nxt:
                self.trie[node].nxt[ch] = len(self.trie)
                self.trie.append(ACNode())
            node = self.trie[node].nxt[ch]
        self.trie[node].out.append(idx)

    def build(self):
        q = deque()
        for ch, v in self.trie[0].nxt.items():
            q.append(v)
        while q:
            u = q.popleft()
            for ch, v in self.trie[u].nxt.items():
                q.append(v)
                f = self.trie[u].fail
                while f and ch not in self.trie[f].nxt:
                    f = self.trie[f].fail
                self.trie[v].fail = self.trie[f].nxt.get(ch, 0)
                self.trie[v].out += self.trie[self.trie[v].fail].out

    def search(self, text: str) -> List[Tuple[int, int]]:
        """반환: (끝나는 위치, 패턴 idx)
        필요시 시작위치 = end - len(pattern[idx]) + 1 로 환산
        """
        res = []
        u = 0
        for i, ch in enumerate(text):
            while u and ch not in self.trie[u].nxt:
                u = self.trie[u].fail
            u = self.trie[u].nxt.get(ch, 0)
            for pid in self.trie[u].out:
                res.append((i, pid))
        return res

# =============================================================================
# 19. Dinic (Maximum Flow)
# =============================================================================

class Dinic:
    def __init__(self, n: int):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.to = []
        self.cap = []

    def _add_edge(self, u: int, v: int, c: int):
        self.to.append(v); self.cap.append(c); self.g[u].append(len(self.to)-1)
    def add_edge(self, u: int, v: int, c: int):
        self._add_edge(u, v, c)
        self._add_edge(v, u, 0)

    def bfs(self, s: int, t: int) -> List[int]:
        level = [-1]*self.n
        q = deque([s]); level[s] = 0
        while q:
            u = q.popleft()
            for ei in self.g[u]:
                if self.cap[ei] > 0:
                    v = self.to[ei]
                    if level[v] == -1:
                        level[v] = level[u] + 1
                        q.append(v)
        return level

    def dfs(self, u: int, t: int, f: int, it: List[int], level: List[int]) -> int:
        if u == t:
            return f
        i = it[u]
        while i < len(self.g[u]):
            ei = self.g[u][i]
            v = self.to[ei]
            if self.cap[ei] > 0 and level[v] == level[u] + 1:
                pushed = self.dfs(v, t, min(f, self.cap[ei]), it, level)
                if pushed:
                    self.cap[ei] -= pushed
                    self.cap[ei^1] += pushed
                    return pushed
            i += 1
            it[u] = i
        return 0

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        while True:
            level = self.bfs(s, t)
            if level[t] == -1:
                break
            it = [0]*self.n
            while True:
                pushed = self.dfs(s, t, INF, it, level)
                if not pushed:
                    break
                flow += pushed
        return flow

# =============================================================================
# 20. Min-Cost Max-Flow (SPFA 기반)
# =============================================================================

class MCMF:
    def __init__(self, n: int):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.to = []
        self.cap = []
        self.cost = []

    def _add_edge(self, u: int, v: int, c: int, w: int):
        self.to.append(v); self.cap.append(c); self.cost.append(w); self.g[u].append(len(self.to)-1)

    def add_edge(self, u: int, v: int, c: int, w: int):
        self._add_edge(u, v, c, w)
        self._add_edge(v, u, 0, -w)

    def min_cost_max_flow(self, s: int, t: int) -> Tuple[int, int]:
        n = self.n
        flow, cost_sum = 0, 0
        while True:
            dist = [INF]*n
            inq = [False]*n
            pv = [-1]*n
            pe = [-1]*n
            q = deque([s]); dist[s] = 0; inq[s] = True
            while q:
                u = q.popleft(); inq[u] = False
                for ei in self.g[u]:
                    if self.cap[ei] > 0:
                        v = self.to[ei]
                        nd = dist[u] + self.cost[ei]
                        if nd < dist[v]:
                            dist[v] = nd; pv[v] = u; pe[v] = ei
                            if not inq[v]:
                                inq[v] = True; q.append(v)
            if dist[t] == INF:
                break
            # 증분 유량 찾기
            aug = INF; v = t
            while v != s:
                ei = pe[v]
                aug = min(aug, self.cap[ei])
                v = pv[v]
            v = t
            while v != s:
                ei = pe[v]
                self.cap[ei] -= aug
                self.cap[ei^1] += aug
                v = pv[v]
            flow += aug
            cost_sum += aug * dist[t]
        return flow, cost_sum

# =============================================================================
# 21. 기하: CCW / 선분 교차 / 볼록껍질(Andrew)
# =============================================================================

Point = Tuple[int, int]

def ccw(a: Point, b: Point, c: Point) -> int:
    x1, y1 = b[0]-a[0], b[1]-a[1]
    x2, y2 = c[0]-a[0], c[1]-a[1]
    val = x1*y2 - x2*y1
    return (val > 0) - (val < 0)  # 1:ccw, -1:cw, 0:collinear

def _on_segment(a: Point, b: Point, p: Point) -> bool:
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

def seg_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    ab = ccw(a, b, c) * ccw(a, b, d)
    cd = ccw(c, d, a) * ccw(c, d, b)
    if ab == 0 and cd == 0:
        # collinear: overlap check
        if a > b: a, b = b, a
        if c > d: c, d = d, c
        return not (b < c or d < a)
    return ab <= 0 and cd <= 0

def convex_hull(pts: List[Point]) -> List[Point]:
    pts = sorted(set(pts))
    if len(pts) <= 1:
        return pts
    def cross(o: Point, a: Point, b: Point) -> int:
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

# =============================================================================
# 22. 행렬 거듭제곱 & 모듈러 조합
# =============================================================================

def mat_mul(A: List[List[int]], B: List[List[int]], mod: int) -> List[List[int]]:
    n = len(A)
    Z = [[0]*n for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Zi = Z[i]
        for k in range(n):
            aik = Ai[k]
            if aik == 0: continue
            Bk = B[k]
            for j in range(n):
                Zi[j] = (Zi[j] + aik * Bk[j]) % mod
    return Z

def mat_pow(A: List[List[int]], e: int, mod: int) -> List[List[int]]:
    n = len(A)
    R = [[int(i==j) for j in range(n)] for i in range(n)]
    B = [row[:] for row in A]
    while e:
        if e & 1:
            R = mat_mul(R, B, mod)
        B = mat_mul(B, B, mod)
        e >>= 1
    return R

# nCr mod p (p is prime)
class CombMod:
    def __init__(self, max_n: int, mod: int):
        self.mod = mod
        self.fact = [1]*(max_n+1)
        for i in range(1, max_n+1):
            self.fact[i] = self.fact[i-1]*i % mod
        self.invfact = [1]*(max_n+1)
        self.invfact[max_n] = pow(self.fact[max_n], mod-2, mod)
        for i in range(max_n, 0, -1):
            self.invfact[i-1] = self.invfact[i]*i % mod
    def nCr(self, n: int, r: int) -> int:
        if r < 0 or r > n: return 0
        return self.fact[n]*self.invfact[r]%self.mod*self.invfact[n-r]%self.mod

# =============================================================================
# 23. Mo's Algorithm (오프라인 질의 스켈레톤)
# =============================================================================

class Mo:
    """배열 a와 [l, r] 질의에 대해 add/remove/answer 훅만 채우면 됩니다.
    예시: 서로 다른 값의 개수, 부분합 등.
    """
    def __init__(self, a: List[int]):
        self.a = a
        self.n = len(a)
        self.cnt = defaultdict(int)
        self.distinct = 0  # 예시: 서로 다른 값 개수

    def add(self, i: int):
        x = self.a[i]
        self.cnt[x] += 1
        if self.cnt[x] == 1:
            self.distinct += 1

    def remove(self, i: int):
        x = self.a[i]
        self.cnt[x] -= 1
        if self.cnt[x] == 0:
            self.distinct -= 1

    def answer(self) -> int:
        return self.distinct

    def solve(self, queries: List[Tuple[int, int]]) -> List[int]:
        B = max(1, int(self.n ** 0.5))
        qs = list(range(len(queries)))
        qs.sort(key=lambda i: (queries[i][0]//B, queries[i][1] if (queries[i][0]//B)%2==0 else -queries[i][1]))
        L = 0; R = -1
        ans = [0]*len(queries)
        for qi in qs:
            l, r = queries[qi]
            while R < r:
                R += 1; self.add(R)
            while R > r:
                self.remove(R); R -= 1
            while L < l:
                self.remove(L); L += 1
            while L > l:
                L -= 1; self.add(L)
            ans[qi] = self.answer()
        return ans

# =============================================================================
# 24. 세그트리 Lazy (구간 치환 assign / 구간 최솟값 RMQ)
# =============================================================================

class SegTreeAssignMin:
    """Range Assign + Range Min Query (0-indexed)
    - 연산: range_assign(l,r,val), range_min(l,r)
    - build O(n), update/query O(log n)
    주의: assign만 지원(+= 미지원). 필요 시 별도 클래스 권장.
    """
    def __init__(self, a: List[int]):
        self.n = len(a)
        self.seg = [INF] * (4*self.n)
        self.has = [False] * (4*self.n)  # lazy flag
        self.lz = [0] * (4*self.n)       # lazy value for assign
        if self.n:
            self._build(1, 0, self.n-1, a)
    def _build(self, idx, l, r, a):
        if l == r:
            self.seg[idx] = a[l]
            return
        m = (l+r)//2
        self._build(idx*2, l, m, a)
        self._build(idx*2+1, m+1, r, a)
        self.seg[idx] = min(self.seg[idx*2], self.seg[idx*2+1])
    def _apply(self, idx, l, r, val):
        self.seg[idx] = val
        self.has[idx] = True
        self.lz[idx] = val
    def _push(self, idx, l, r):
        if not self.has[idx] or l == r:
            return
        m = (l+r)//2
        self._apply(idx*2, l, m, self.lz[idx])
        self._apply(idx*2+1, m+1, r, self.lz[idx])
        self.has[idx] = False
    def _update(self, idx, l, r, ql, qr, val):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            self._apply(idx, l, r, val)
            return
        self._push(idx, l, r)
        m = (l+r)//2
        self._update(idx*2, l, m, ql, qr, val)
        self._update(idx*2+1, m+1, r, ql, qr, val)
        self.seg[idx] = min(self.seg[idx*2], self.seg[idx*2+1])
    def _query(self, idx, l, r, ql, qr):
        if qr < l or r < ql:
            return INF
        if ql <= l and r <= qr:
            return self.seg[idx]
        self._push(idx, l, r)
        m = (l+r)//2
        return min(self._query(idx*2, l, m, ql, qr),
                   self._query(idx*2+1, m+1, r, ql, qr))
    def range_assign(self, l: int, r: int, val: int):
        if l > r: return
        self._update(1, 0, self.n-1, l, r, val)
    def range_min(self, l: int, r: int) -> int:
        if l > r: return INF
        return self._query(1, 0, self.n-1, l, r)

# =============================================================================
# 25. LCA + 거리가중 트리: 거리/경로 복원 유틸
# =============================================================================

class LCAWeighted:
    """무방향 가중 트리 (1-indexed)
    제공: lca(u,v), dist(u,v), path(u,v) (상하향 단순 복원)
    g[u] = [(v, w)]
    """
    def __init__(self, n: int, g: List[List[Tuple[int,int]]], root: int = 1):
        self.n = n
        self.LOG = (n).bit_length()
        self.up = [[0]*(n+1) for _ in range(self.LOG)]
        self.depth = [0]*(n+1)
        self.dist0 = [0]*(n+1)  # root로부터 누적 거리
        self.parent = [0]*(n+1)
        self._bfs_build(g, root)
        for k in range(1, self.LOG):
            for v in range(1, n+1):
                self.up[k][v] = self.up[k-1][ self.up[k-1][v] ]
    def _bfs_build(self, g, root):
        from collections import deque
        q = deque([root])
        self.up[0][root] = 0
        self.parent[root] = 0
        self.depth[root] = 0
        seen = [False]*(self.n+1)
        seen[root] = True
        while q:
            u = q.popleft()
            for v, w in g[u]:
                if not seen[v]:
                    seen[v] = True
                    self.parent[v] = u
                    self.up[0][v] = u
                    self.depth[v] = self.depth[u] + 1
                    self.dist0[v] = self.dist0[u] + w
                    q.append(v)
    def lca(self, a: int, b: int) -> int:
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        # raise a
        diff = self.depth[a] - self.depth[b]
        k = 0
        while diff:
            if diff & 1:
                a = self.up[k][a]
            diff >>= 1; k += 1
        if a == b: return a
        for k in range(self.LOG-1, -1, -1):
            if self.up[k][a] != self.up[k][b]:
                a = self.up[k][a]
                b = self.up[k][b]
        return self.up[0][a]
    def dist(self, a: int, b: int) -> int:
        c = self.lca(a, b)
        return self.dist0[a] + self.dist0[b] - 2*self.dist0[c]
    def path(self, a: int, b: int) -> List[int]:
        """경로 노드 목록 반환(부모 포인터로 단순 복원) O(length)
        큰 그래프에서는 HLD 경로 질의 사용 권장
        """
        c = self.lca(a, b)
        up_path = []
        x = a
        while x != c:
            up_path.append(x); x = self.parent[x]
        up_path.append(c)
        down_path = []
        y = b
        while y != c:
            down_path.append(y); y = self.parent[y]
        down_path.reverse()
        return up_path + down_path

# =============================================================================
# 26. 문자열: Aho–Corasick(요약) + Z-Algorithm
# =============================================================================

# (요약) 이미 위에서 정의됨 - AhoCorasick 클래스는 18번 섹션 참고

# Z-Algorithm: z[i] = s와 s[i:]의 lcp 길이

def z_algorithm(s: str) -> List[int]:
    n = len(s)
    z = [0]*n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    z[0] = n
    return z

# =============================================================================
# 27. Sparse Table(RMQ) + Heavy-Light Decomposition(경로 쿼리: 합/최솟값)
# =============================================================================

# SparseTableMin: 이미 16번 섹션에서 정의됨 - 중복 제거

# --- 세그트리(점 갱신 + 구간 합/최솟값) ---
class _SegSum:
    def __init__(self, a: List[int]):
        n = len(a)
        self.N = 1
        while self.N < n: self.N <<= 1
        self.seg = [0]*(2*self.N)
        for i, v in enumerate(a): self.seg[self.N+i] = v
        for i in range(self.N-1, 0, -1): self.seg[i] = self.seg[i*2] + self.seg[i*2+1]
    def update(self, i: int, v: int):
        i += self.N; self.seg[i] = v; i >>= 1
        while i: self.seg[i] = self.seg[i*2] + self.seg[i*2+1]; i >>= 1
    def query(self, l: int, r: int) -> int:
        l += self.N; r += self.N; res = 0
        while l <= r:
            if l & 1: res += self.seg[l]; l += 1
            if not (r & 1): res += self.seg[r]; r -= 1
            l >>= 1; r >>= 1
        return res

class _SegMin:
    def __init__(self, a: List[int]):
        n = len(a)
        self.N = 1
        while self.N < n: self.N <<= 1
        self.seg = [INF]*(2*self.N)
        for i, v in enumerate(a): self.seg[self.N+i] = v
        for i in range(self.N-1, 0, -1): self.seg[i] = min(self.seg[i*2], self.seg[i*2+1])
    def update(self, i: int, v: int):
        i += self.N; self.seg[i] = v; i >>= 1
        while i: self.seg[i] = min(self.seg[i*2], self.seg[i*2+1]); i >>= 1
    def query(self, l: int, r: int) -> int:
        l += self.N; r += self.N; res = INF
        while l <= r:
            if l & 1: res = min(res, self.seg[l]); l += 1
            if not (r & 1): res = min(res, self.seg[r]); r -= 1
            l >>= 1; r >>= 1
        return res

class HLD:
    """Heavy-Light Decomposition for path queries (1-indexed tree)
    - 두 가지 세그트리를 내부에 보유: 합/최솟값
    - 점 갱신(update_point), 경로 쿼리(path_sum/path_min)
    사용 전 build(values) 호출 (values[v]는 노드 v의 초기값)
    g: 인접 리스트(무가중)
    """
    def __init__(self, n: int, g: List[List[int]], root: int = 1):
        self.n = n; self.g = g; self.root = root
        self.sz = [0]*(n+1)
        self.par = [0]*(n+1)
        self.depth = [0]*(n+1)
        self.hch = [0]*(n+1)
        self.head = [0]*(n+1)
        self.tin = [0]*(n+1)
        self.rid = [0]*(n+1)
        self._dfs_sz(root, 0)
        self._cur = 0
        self._dfs_hld(root, root)
        self._seg_sum = None
        self._seg_min = None
    def _dfs_sz(self, u: int, p: int):
        self.sz[u] = 1; self.par[u] = p
        maxsz, heavy = 0, 0
        for v in self.g[u]:
            if v == p: continue
            self.depth[v] = self.depth[u] + 1
            self._dfs_sz(v, u)
            if self.sz[v] > maxsz:
                maxsz, heavy = self.sz[v], v
            self.sz[u] += self.sz[v]
        self.hch[u] = heavy
    def _dfs_hld(self, u: int, h: int):
        self.head[u] = h
        self.tin[u] = self._cur
        self.rid[self._cur] = u
        self._cur += 1
        if self.hch[u]:
            self._dfs_hld(self.hch[u], h)
            for v in self.g[u]:
                if v != self.par[u] and v != self.hch[u]:
                    self._dfs_hld(v, v)
    def build(self, values: List[int]):
        arr = [0]*self.n
        for v in range(1, self.n+1):
            arr[self.tin[v]] = values[v]
        self._seg_sum = _SegSum(arr)
        self._seg_min = _SegMin(arr)
    def update_point(self, v: int, new_val: int):
        i = self.tin[v]
        self._seg_sum.update(i, new_val)
        self._seg_min.update(i, new_val)
    def _path_op(self, u: int, v: int, op):
        res = None
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            h = self.head[u]
            cur = op(self.tin[h], self.tin[u])
            res = cur if res is None else op.merge(res, cur)
            u = self.par[h]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        cur = op(self.tin[u], self.tin[v])
        res = cur if res is None else op.merge(res, cur)
        return res
    class _OpSum:
        def __init__(self, seg): self.seg = seg
        def __call__(self, l, r): return self.seg.query(l, r)
        @staticmethod
        def merge(a, b): return a + b
    class _OpMin:
        def __init__(self, seg): self.seg = seg
        def __call__(self, l, r): return self.seg.query(l, r)
        @staticmethod
        def merge(a, b): return a if a <= b else b
    def path_sum(self, u: int, v: int) -> int:
        return self._path_op(u, v, HLD._OpSum(self._seg_sum))
    def path_min(self, u: int, v: int) -> int:
        return self._path_op(u, v, HLD._OpMin(self._seg_min))

# =============================================================================
# 28. SCC(강결합요소: Kosaraju) + 2-SAT(간단 구현)
# =============================================================================

class KosarajuSCC:
    def __init__(self, n: int):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.rg = [[] for _ in range(n)]
    def add_edge(self, u: int, v: int):
        self.g[u].append(v)
        self.rg[v].append(u)
    def scc(self) -> Tuple[int, List[int]]:
        sys.setrecursionlimit(1_000_000)
        vis = [False]*self.n
        order = []
        def dfs(u):
            vis[u] = True
            for v in self.g[u]:
                if not vis[v]: dfs(v)
            order.append(u)
        for i in range(self.n):
            if not vis[i]: dfs(i)
        comp = [-1]*self.n
        cid = 0
        def rdfs(u):
            comp[u] = cid
            for v in self.rg[u]:
                if comp[v] == -1: rdfs(v)
        for u in reversed(order):
            if comp[u] == -1:
                rdfs(u)
                cid += 1
        return cid, comp

class TwoSAT:
    def __init__(self, n: int):
        self.n = n
        self.scc = KosarajuSCC(2*n)
    @staticmethod
    def _id(x: int, val: bool) -> int:
        return 2*x ^ (1 if val else 0)
    def add_or(self, a: int, aval: bool, b: int, bval: bool):
        # (a==aval) or (b==bval)  <=> (!a->b) & (!b->a)
        self.scc.add_edge(self._id(a, not aval), self._id(b, bval))
        self.scc.add_edge(self._id(b, not bval), self._id(a, aval))
    def add_true(self, a: int, aval: bool):
        self.scc.add_edge(self._id(a, not aval), self._id(a, aval))
    def solve(self) -> Optional[List[bool]]:
        _, comp = self.scc.scc()
        ans = [False]*self.n
        for x in range(self.n):
            if comp[2*x] == comp[2*x^1]:
                return None
        order = sorted(range(2*self.n), key=lambda i: comp[i], reverse=True)
        val = [False]*(2*self.n)
        for v in order:
            if not val[v] and not val[v^1]:
                val[v] = True
        for x in range(self.n):
            ans[x] = val[2*x^1]
        return ans

# =============================================================================
# 29. 네트워크 플로우: Dinic(요약) + Edmonds–Karp
# =============================================================================

# Dinic: 이미 19번 섹션에서 정의됨 - 중복 제거

class EdmondsKarp:
    def __init__(self, n: int):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.to, self.cap = [], []
    def _add_edge(self, u, v, c):
        self.to.append(v); self.cap.append(c); self.g[u].append(len(self.to)-1)
    def add_edge(self, u, v, c):
        self._add_edge(u, v, c)
        self._add_edge(v, u, 0)
    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        n = self.n
        while True:
            pv = [-1]*n; pe = [-1]*n
            q = deque([s]); pv[s] = s
            while q and pv[t] == -1:
                u = q.popleft()
                for ei in self.g[u]:
                    if self.cap[ei] > 0:
                        v = self.to[ei]
                        if pv[v] == -1:
                            pv[v] = u; pe[v] = ei; q.append(v)
                            if v == t: break
            if pv[t] == -1: break
            aug = INF; v = t
            while v != s:
                ei = pe[v]
                aug = min(aug, self.cap[ei])
                v = pv[v]
            v = t
            while v != s:
                ei = pe[v]
                self.cap[ei] -= aug
                self.cap[ei^1] += aug
                v = pv[v]
            flow += aug
        return flow

# =============================================================================
# 사용 예시 (주석)  (15~23번)
# =============================================================================
# 1) 2-SAT
# n = 3
# ts = TwoSAT(n)
# ts.add_or(0, True, 1, False)   # x0 or !x1
# ts.add_or(1, True, 2, True)    # x1 or x2
# sol = ts.solve()
# print(sol)  # None(불가능) 또는 [bool]*n
#
# 2) Dinic
# mf = Dinic(N)
# mf.add_edge(u, v, c)
# print(mf.max_flow(s, t))
#
# 3) Aho–Corasick
# ac = AhoCorasick()
# for i, w in enumerate(patterns):
#     ac.add(w, i)
# ac.build()
# matches = ac.search(text)
#
# 4) Sparse Table
# st = SparseTableMin(arr)
# print(st.query(l, r))


# =============================================================================
# 사용 예시 (주석)
# =============================================================================
# 24) assign-min 세그트리
# st = SegTreeAssignMin([5,1,7,3])
# st.range_assign(1,3,2)
# print(st.range_min(0,3))
#
# 25) LCAWeighted
# g = [[] for _ in range(n+1)]
# g[u].append((v,w)); g[v].append((u,w))
# lca = LCAWeighted(n, g, 1)
# print(lca.dist(u,v))
# print(lca.path(u,v))
#
# 26) Z-Algorithm
# z = z_algorithm("pattern#text")
#
# 27) HLD
# hld = HLD(n, tree, 1); hld.build(values)
# print(hld.path_sum(u,v)); hld.update_point(x, new)
#
# 28) 2-SAT
# ts = TwoSAT(n); ts.add_or(0,True,1,False); print(ts.solve())
#
# 29) Edmonds–Karp
# ek = EdmondsKarp(N); ek.add_edge(u,v,c); print(ek.max_flow(s,t))

# =============================================================================
# 30. 추가 고성능 자료구조 - 새로 추가됨
# =============================================================================

# Sqrt Decomposition (Mo's Algorithm 대안)
class SqrtDecomposition:
    """Square Root Decomposition for range queries - O(sqrt(n)) per query"""
    def __init__(self, a: List[int]):
        self.n = len(a)
        self.block_size = int(self.n ** 0.5) + 1
        self.blocks = (self.n + self.block_size - 1) // self.block_size
        self.a = a[:]
        self.lazy = [0] * self.blocks
        
    def update(self, l: int, r: int, val: int):
        """Add val to range [l, r]"""
        start_block = l // self.block_size
        end_block = r // self.block_size
        
        if start_block == end_block:
            for i in range(l, r + 1):
                self.a[i] += val
        else:
            # Left partial block
            for i in range(l, (start_block + 1) * self.block_size):
                if i < self.n:
                    self.a[i] += val
            
            # Middle full blocks
            for block in range(start_block + 1, end_block):
                self.lazy[block] += val
            
            # Right partial block
            for i in range(end_block * self.block_size, r + 1):
                if i < self.n:
                    self.a[i] += val
    
    def query(self, l: int, r: int) -> int:
        """Sum of range [l, r]"""
        result = 0
        for i in range(l, r + 1):
            if i < self.n:
                block_id = i // self.block_size
                result += self.a[i] + self.lazy[block_id]
        return result

# 이진 인덱스드 트리 2D (2D BIT)
class Fenwick2D:
    """2D Binary Indexed Tree for 2D range sum queries"""
    __slots__ = ('n', 'm', 'bit')
    
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.bit = [[0] * (m + 1) for _ in range(n + 1)]
    
    def add(self, x: int, y: int, delta: int):
        """Add delta to (x, y) - 1-indexed"""
        i = x
        while i <= self.n:
            j = y
            while j <= self.m:
                self.bit[i][j] += delta
                j += j & -j
            i += i & -i
    
    def sum(self, x: int, y: int) -> int:
        """Sum of rectangle (1,1) to (x,y) - 1-indexed"""
        result = 0
        i = x
        while i > 0:
            j = y
            while j > 0:
                result += self.bit[i][j]
                j -= j & -j
            i -= i & -i
        return result
    
    def range_sum(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Sum of rectangle (x1,y1) to (x2,y2) - 1-indexed"""
        return (self.sum(x2, y2) - self.sum(x1-1, y2) - 
                self.sum(x2, y1-1) + self.sum(x1-1, y1-1))

# 최적화된 롤링 해시
class RollingHash:
    """Rolling Hash for string matching - optimized version"""
    def __init__(self, s: str, base: int = 31, mod: int = 10**9 + 7):
        self.s = s
        self.n = len(s)
        self.base = base
        self.mod = mod
        
        # Precompute powers and prefix hashes
        self.pow = [1] * (self.n + 1)
        self.hash = [0] * (self.n + 1)
        
        for i in range(self.n):
            self.pow[i + 1] = (self.pow[i] * base) % mod
            self.hash[i + 1] = (self.hash[i] * base + ord(s[i])) % mod
    
    def get_hash(self, l: int, r: int) -> int:
        """Get hash of substring s[l:r+1] - 0-indexed"""
        return (self.hash[r + 1] - self.hash[l] * self.pow[r - l + 1]) % self.mod
    
    def compare(self, l1: int, r1: int, l2: int, r2: int) -> bool:
        """Compare two substrings"""
        return self.get_hash(l1, r1) == self.get_hash(l2, r2)

# =============================================================================
# 사용 예시 (주석) - 새로운 자료구조들
# =============================================================================
# 30) Sqrt Decomposition
# sqrt_ds = SqrtDecomposition([1,2,3,4,5])
# sqrt_ds.update(1, 3, 10)  # Add 10 to range [1,3]
# print(sqrt_ds.query(0, 4))  # Sum of entire array
#
# 31) 2D BIT
# bit2d = Fenwick2D(100, 100)
# bit2d.add(10, 20, 5)  # Add 5 to position (10,20)
# print(bit2d.range_sum(1, 1, 50, 50))  # Sum of rectangle
#
# 32) Rolling Hash
# rh = RollingHash("abcdef")
# hash1 = rh.get_hash(0, 2)  # Hash of "abc"
# hash2 = rh.get_hash(1, 3)  # Hash of "bcd"
# same = rh.compare(0, 2, 3, 5)  # Compare "abc" with "def"
