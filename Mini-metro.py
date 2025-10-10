"""
Mini Metro-style line planner + simulator (simplified)
-----------------------------------------------------
목표: 주어진 정거장/수요/최대 노선 수(K) 하에서, 노선이 '비분기(단일 경로)' 조건을 만족하도록
노선을 구성하고, 간단한 시뮬레이션으로 총 완료 시간(모든 승객 배송 완료 시간)을 최소화하는 설계를 탐색.

가정/제약(현실과 차이가 있는 단순화 포함):
- 정거장은 평면 위 (x, y) 좌표로 고정.
- 손님은 시작 정거장과 정확한 목적지 정거장(같은 정거장은 제외)을 갖는다.
- 노선은 서로 다른 정거장을 잇는 '단순 경로(simple path)'이며 분기 없음.
- 여러 노선이 하나의 정거장을 공유할 수 있으며 환승 가능.
- 각 노선에 배치된 열차 수는 동일(기본값: 1대), 열차 용량은 10명.
- 시간은 Δt 고정 간격으로 이산 시뮬레이션, 열차 속도/정차시간/승하차 시간은 상수.
- 승객은 환승 시 다음 열차를 기다린다(대기열 FIFO).
- 목적 함수는 '모든 승객 배송이 완료되는 시간(완료 makespan)'이며, 2차 지표로 평균 대기/여행 시간도 계산.

주의: 이 코드는 연구용/프로토타입 수준이며, 정확한 게임 규칙과 차이가 있다.
      탐색(로컬 서치) 반복/입력 규모에 따라 계산량이 커질 수 있다.

사용 방법 예:
planner = Planner.random_instance(n_stations=20, n_passengers=400, seed=42)
best = planner.optimize(k_lines=3, iter_outer=50, iter_inner=60)
best.report()

필요 패키지: 표준 라이브러리만 사용
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from pathlib import Path
import os
import math
import random
import itertools
import statistics


# ============================
# 데이터 모델
# ============================
@dataclass
class Station:
    id: int
    x: float
    y: float

@dataclass
class Passenger:
    origin: int
    dest: int
    created_t: float = 0.0
    pickup_t: Optional[float] = None
    drop_t: Optional[float] = None

@dataclass
class Line:
    stations: List[int]
    trains: List[float] = field(default_factory=list)
    directions: List[int] = field(default_factory=list)

    def copy(self) -> 'Line':
        return Line(self.stations[:], self.trains[:], self.directions[:])

@dataclass
class Network:
    stations: List[Station]
    lines: List[Line]

# ============================
# 유틸
# ============================

def dist(a: Station, b: Station) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def path_length(path: List[int], stations: List[Station]) -> float:
    s = 0.0
    for a, b in zip(path, path[1:]):
        s += dist(stations[a], stations[b])
    return s


def line_length(line: Line, stations: List[Station]) -> float:
    return path_length(line.stations, stations)


# 최근접 이웃 기반 단순 경로 구성
def order_as_path(node_ids: List[int], stations: List[Station]) -> List[int]:
    if not node_ids:
        return []
    best_pair, best_d = None, -1.0
    for a, b in itertools.combinations(node_ids, 2):
        d = dist(stations[a], stations[b])
        if d > best_d:
            best_d, best_pair = d, (a, b)
    start = best_pair[0] if best_pair else node_ids[0]

    remaining = set(node_ids)
    path = [start]
    remaining.remove(start)
    while remaining:
        last = path[-1]
        nxt = min(remaining, key=lambda nid: dist(stations[last], stations[nid]))
        path.append(nxt)
        remaining.remove(nxt)
    return path


# 2-opt 로컬 최적화
def two_opt_path(path: List[int], stations: List[Station], rounds: int = 20) -> List[int]:
    best = path[:]
    best_len = path_length(best, stations)
    n = len(best)
    for _ in range(rounds):
        improved = False
        for i in range(1, n-2):
            for j in range(i+1, n-1):
                if j - i <= 1:
                    continue
                new_path = best[:i] + best[i:j][::-1] + best[j:]
                new_len = path_length(new_path, stations)
                if new_len + 1e-9 < best_len:
                    best, best_len = new_path, new_len
                    improved = True
        if not improved:
            break
    return best


# ============================
# 시뮬레이션(왕복 운행)
# ============================
class Simulator:
    def __init__(self,
                 network: Network,
                 passengers: List[Passenger],
                 speed: float = 1.0,
                 dwell_time: float = 5.0,
                 dt: float = 1.0,
                 capacity: int = 10,
                 trains_per_line: int = 1):
        self.network = network
        self.passengers = passengers
        self.speed = speed
        self.dwell_time = dwell_time
        self.dt = dt
        self.capacity = capacity
        self.trains_per_line = trains_per_line

        # 길이 2 미만 라인 제거
        self.network.lines = [ln for ln in self.network.lines if len(ln.stations) >= 2]
        if not self.network.lines:
            raise ValueError("No valid lines (need >= 2 stations per line)")

        # 대기열 초기화
        self.waiting: Dict[int, List[int]] = {s.id: [] for s in network.stations}
        for idx, p in enumerate(passengers):
            self.waiting[p.origin].append(idx)

        # 열차 적재 목록
        self.train_loads: List[List[int]] = []

        # ---- 열차 초기화: 길이+수요 기반 배분 ----
        total_budget = max(1, self.trains_per_line * len(self.network.lines))

        lengths = [line_length(ln, self.network.stations) for ln in self.network.lines]
        Lsum = sum(lengths) or 1.0

        line_st_sets = [set(ln.stations) for ln in self.network.lines]
        demands = [0 for _ in self.network.lines]
        for p in self.passengers:
            for i, stset in enumerate(line_st_sets):
                if p.origin in stset or p.dest in stset:
                    demands[i] += 1
        Dsum = sum(demands) or 1.0

        alpha = 0.5  # 길이/수요 가중 혼합 비율
        weights = [alpha*(lengths[i]/Lsum) + (1-alpha)*(demands[i]/Dsum) for i in range(len(self.network.lines))]

        base = [1 for _ in self.network.lines]
        remain = max(0, total_budget - len(self.network.lines))
        shares = [int(round(remain * w)) for w in weights]
        diff = remain - sum(shares)
        order = sorted(range(len(self.network.lines)), key=lambda i: weights[i], reverse=True)
        for k in range(abs(diff)):
            idx = order[k % len(order)]
            shares[idx] += 1 if diff > 0 else -1
        n_trains_per_line = [base[i] + max(0, shares[i]) for i in range(len(self.network.lines))]

        # 실제 배치(각 라인 균등 간격)
        for li, line in enumerate(self.network.lines):
            line.trains = []
            line.directions = []
            line_len_seg = max(1, len(line.stations) - 1)
            for t in range(n_trains_per_line[li]):
                pos = (t / max(1, n_trains_per_line[li])) * line_len_seg
                line.trains.append(pos)
                line.directions.append(+1)
                self.train_loads.append([])

        # 열차 소유자 인덱싱
        self.train_owners: List[Tuple[int, int]] = []
        for li, line in enumerate(self.network.lines):
            for ti in range(len(line.trains)):
                self.train_owners.append((li, ti))

        # 역-라인 매핑
        self.station_to_lines: Dict[int, List[int]] = {s.id: [] for s in self.network.stations}
        for li, line in enumerate(self.network.lines):
            for sid in line.stations:
                if li not in self.station_to_lines[sid]:
                    self.station_to_lines[sid].append(li)

        self._build_adjacency()
        self._precompute_segments()

    # ----- 그래프/세그먼트 전처리 -----
    def _build_adjacency(self) -> None:
        self.adj: Dict[int, List[int]] = {s.id: [] for s in self.network.stations}
        for line in self.network.lines:
            for a, b in zip(line.stations, line.stations[1:]):
                if b not in self.adj[a]:
                    self.adj[a].append(b)
                if a not in self.adj[b]:
                    self.adj[b].append(a)

    def _precompute_segments(self) -> None:
        self.line_seglen: List[List[float]] = []
        self.line_cumlen: List[List[float]] = []
        for line in self.network.lines:
            segs = []
            for a, b in zip(line.stations, line.stations[1:]):
                A = self.network.stations[a]
                B = self.network.stations[b]
                segs.append(math.hypot(A.x - B.x, A.y - B.y))
            self.line_seglen.append(segs)
            cum = [0.0]
            for L in segs:
                cum.append(cum[-1] + L)
            self.line_cumlen.append(cum)

    # ----- 경로 탐색 -----
    def next_hop(self, curr: int, dest: int) -> Optional[int]:
        if curr == dest:
            return None
        q = [curr]
        prev = {curr: None}
        while q:
            u = q.pop(0)
            if u == dest:
                break
            for v in self.adj.get(u, []):
                if v not in prev:
                    prev[v] = u
                    q.append(v)
        if dest not in prev:
            return None
        path = []
        v = dest
        while v is not None:
            path.append(v)
            v = prev[v]
        path.reverse()
        return path[1] if len(path) >= 2 else None

    def _bfs_distance(self, u: int, v: int) -> Optional[int]:
        if u == v:
            return 0
        q = [u]
        dist_map = {u: 0}
        while q:
            x = q.pop(0)
            for y in self.adj.get(x, []):
                if y not in dist_map:
                    dist_map[y] = dist_map[x] + 1
                    if y == v:
                        return dist_map[y]
                    q.append(y)
        return None

    def next_station_of_this_train(self, li: int, ti: int, station_index: int) -> Optional[int]:
        """현재 방향 기준 다음 역. 끝점이면 None(왕복 전환은 simulate에서 결정)."""
        line = self.network.lines[li]
        n = len(line.stations)
        direction = line.directions[ti]
        nxt_idx = station_index + (1 if direction >= 0 else -1)
        if 0 <= nxt_idx < n:
            return line.stations[nxt_idx]
        return None

    # ----- 승하차 -----
    def perform_stop(self, li: int, ti: int, station_id: int, now_t: float,
                      next_target: Optional[int]) -> Tuple[int, int]:
        load = self.train_loads[self.train_global_index(li, ti)]
        n_alight = 0
        remain = []
        for pid in load:
            p = self.passengers[pid]
            if p.dest == station_id:
                p.drop_t = now_t
                n_alight += 1
            else:
                nh = self.next_hop(station_id, p.dest)
                if next_target is None or nh is None or nh != next_target:
                    self.waiting[station_id].append(pid)
                else:
                    remain.append(pid)
        load[:] = remain

        queue = self.waiting[station_id]
        n_board = 0
        if next_target is None or not queue:
            return n_alight, n_board

        capacity_left = self.capacity - len(load)
        if capacity_left <= 0:
            return n_alight, n_board

        # 방향 일치 + 우선순위(오래 대기, 남은 hop)
        eligible = []
        for pid in queue:
            dest = self.passengers[pid].dest
            nh = self.next_hop(station_id, dest)
            if nh == next_target:
                wait = max(0.0, now_t - self.passengers[pid].created_t)
                rh = self._bfs_distance(station_id, dest) or 0
                eligible.append((pid, wait, rh))
        if not eligible:
            return n_alight, n_board

        eligible.sort(key=lambda x: (-x[1], -x[2]))
        take = min(capacity_left, len(eligible))
        boarded = [pid for pid, _, _ in eligible[:take]]
        sel = set(boarded)
        self.waiting[station_id] = [pid for pid in queue if pid not in sel]
        for pid in boarded:
            self.passengers[pid].pickup_t = self.passengers[pid].pickup_t or now_t
        load.extend(boarded)
        n_board = take
        return n_alight, n_board

    # ----- 시뮬레이션 루프 -----
    def simulate(self, max_time: float = 3600*4) -> Dict[str, float]:
        t = 0.0
        self.dwell_counters: Dict[Tuple[int, int], float] = {}
        ended_by_completion = False

        def arrive_station(li: int, ti: int, station_id: int, next_target: Optional[int], now_t: float):
            base = max(1.0, self.dwell_time * 0.4)
            per_pax = 0.7
            n_alight, n_board = self.perform_stop(li, ti, station_id, now_t, next_target)
            dwell = base + per_pax * (n_alight + n_board)
            self.dwell_counters[(li, ti)] = dwell

        # 초기 세그먼트 위치
        self._segpos: Dict[Tuple[int, int], Tuple[int, float]] = {}
        for li, line in enumerate(self.network.lines):
            nseg = max(1, len(line.stations) - 1)
            for ti, prog in enumerate(line.trains):
                seg = int(min(max(math.floor(prog), 0), nseg - 1))
                self._segpos[(li, ti)] = (seg, 0.0)

        while t < max_time:
            if all(p.drop_t is not None for p in self.passengers):
                ended_by_completion = True
                break

            for li, line in enumerate(self.network.lines):
                seglens = self.line_seglen[li]
                for ti in range(len(line.trains)):
                    key = (li, ti)
                    if self.dwell_counters.get(key, 0.0) > 0.0:
                        self.dwell_counters[key] = max(0.0, self.dwell_counters[key] - self.dt)
                        continue

                    seg, off = self._segpos[key]
                    direction = line.directions[ti]
                    seglen = seglens[seg] if 0 <= seg < len(seglens) else 0.0
                    advance = self.speed * self.dt

                    while advance > 0:
                        remain = seglen - off if 0 <= seg < len(seglens) else 0.0
                        if remain <= 1e-9:
                            # 정거장 도착
                            st_idx = seg + 1 if direction >= 0 else seg
                            station_id = line.stations[st_idx]

                            # 전환 여부/다음 목표역 계산(왕복)
                            at_end_forward = (direction >= 0 and st_idx == len(line.stations) - 1)
                            at_end_backward = (direction < 0 and st_idx == 0)
                            next_dir = -direction if (at_end_forward or at_end_backward) else direction
                            nxt_idx = st_idx + (1 if next_dir >= 0 else -1)
                            next_target = line.stations[nxt_idx] if 0 <= nxt_idx < len(line.stations) else None

                            # 전환 후 목표를 기준으로 승하차
                            arrive_station(li, ti, station_id, next_target, t)

                            # 방향/세그 갱신
                            line.directions[ti] = next_dir
                            if next_dir >= 0:
                                seg = min(st_idx, len(seglens) - 1)
                            else:
                                seg = max(st_idx - 1, 0)
                            off = 0.0
                            seglen = seglens[seg] if 0 <= seg < len(seglens) else 0.0
                            break  # 이번 tick은 정차로 종료
                        else:
                            step = min(advance, remain)
                            off += step
                            advance -= step
                            if abs(off - seglen) <= 1e-9:
                                continue  # 상단에서 도착 처리

                    self._segpos[key] = (seg, off)

            t += self.dt

        drops = [p.drop_t for p in self.passengers if p.drop_t is not None]
        picks = [p.pickup_t for p in self.passengers if p.pickup_t is not None]
        done_ratio = len(drops) / max(1, len(self.passengers))
        # if ended_by_completion and drops:
        #     t = max(drops)
        return {
            "sim_time": t,
            "done_ratio": done_ratio,
            "makespan": max(drops) if drops else float('inf'),
            "avg_wait": statistics.mean([(p.pickup_t - p.created_t) for p in self.passengers if p.pickup_t is not None]) if picks else float('inf'),
            "avg_trip": statistics.mean([(p.drop_t - (p.pickup_t or p.created_t)) for p in self.passengers if p.drop_t is not None]) if drops else float('inf'),
        }

    def train_global_index(self, li: int, ti: int) -> int:
        idx = 0
        for i in range(li):
            idx += len(self.network.lines[i].trains)
        idx += ti
        return idx

# ============================
# 설계(휴리스틱) + 최적화
# ============================
class Planner:
    def __init__(self, stations: List[Station], passengers: List[Passenger]):
        self.stations = stations
        self.passengers = passengers

    @staticmethod
    def random_instance(n_stations: int = 20, n_passengers: int = 400, seed: int = 0,
                        width: float = 100.0, height: float = 100.0) -> 'Planner':
        rnd = random.Random(seed)
        stations = [Station(i, rnd.uniform(0, width), rnd.uniform(0, height)) for i in range(n_stations)]
        passengers: List[Passenger] = []
        for _ in range(n_passengers):
            o = rnd.randrange(n_stations)
            d = o
            while d == o:
                d = rnd.randrange(n_stations)
            passengers.append(Passenger(origin=o, dest=d, created_t=0.0))
        return Planner(stations, passengers)

    # 초기 라인 구성
    def initial_lines(self, k_lines: int, seed: int = 0) -> List[Line]:
        rnd = random.Random(seed)
        centroids = rnd.sample(self.stations, k_lines)
        for _ in range(5):
            buckets = [[] for _ in range(k_lines)]
            for s in self.stations:
                ci = min(range(k_lines), key=lambda i: dist(s, centroids[i]))
                buckets[ci].append(s.id)
            new_centroids = []
            for i in range(k_lines):
                if not buckets[i]:
                    new_centroids.append(centroids[i])
                else:
                    xs = [self.stations[sid].x for sid in buckets[i]]
                    ys = [self.stations[sid].y for sid in buckets[i]]
                    new_centroids.append(Station(-1, sum(xs)/len(xs), sum(ys)/len(ys)))
            centroids = new_centroids
        lines = []
        for bucket in buckets:
            if not bucket:
                continue
            path = order_as_path(bucket, self.stations)
            path = two_opt_path(path, self.stations, rounds=15)
            lines.append(Line(stations=path, trains=[], directions=[]))
        self._ensure_connectivity(lines)
        self._ensure_multi_hubs(lines, min_shared=2)
        return lines

    def evaluate(self, lines: List[Line], sim_time: float = 3600.0, speed: float = 1.0,
                 dwell_time: float = 5.0, dt: float = 1.0, trains_per_line: int = 1) -> Dict[str, float]:
        net = Network(self.stations, [ln.copy() for ln in lines])
        sim = Simulator(net, [Passenger(p.origin, p.dest, p.created_t) for p in self.passengers],
                        speed=speed, dwell_time=dwell_time, dt=dt, trains_per_line=trains_per_line)
        return sim.simulate(max_time=sim_time)

    # 로컬 서치
    def optimize(self, k_lines: int, iter_outer: int = 40, iter_inner: int = 60,
                 speed: float = 1.0, dwell_time: float = 5.0, dt: float = 1.0,
                 trains_per_line: int = 1, seed: int = 0) -> 'PlanResult':
        rnd = random.Random(seed)
        lines = self.initial_lines(k_lines, seed=seed)
        best_lines = [ln.copy() for ln in lines]

        SIM_T = 3600.0
        def _cost(metrics):
            return metrics["makespan"] + (1.0 - metrics["done_ratio"]) * SIM_T * 1000.0

        best_metrics = self.evaluate(best_lines, sim_time=SIM_T, speed=speed, dwell_time=dwell_time, dt=dt, trains_per_line=trains_per_line)
        best_score = _cost(best_metrics)

        for _ in range(iter_outer):
            curr = [ln.copy() for ln in best_lines]
            for _ in range(iter_inner):
                move_type = rnd.choice(["two_opt", "swap", "move"])  # 3종 변이
                if move_type == "two_opt":
                    li = rnd.randrange(len(curr))
                    path = curr[li].stations
                    if len(path) > 4:
                        curr[li].stations = two_opt_path(path, self.stations, rounds=5)
                elif move_type == "swap" and len(curr) >= 2:
                    l1, l2 = rnd.sample(range(len(curr)), 2)
                    if curr[l1].stations and curr[l2].stations:
                        i = rnd.randrange(len(curr[l1].stations))
                        j = rnd.randrange(len(curr[l2].stations))
                        curr[l1].stations[i], curr[l2].stations[j] = curr[l2].stations[j], curr[l1].stations[i]
                elif move_type == "move" and len(curr) >= 2:
                    src, dst = rnd.sample(range(len(curr)), 2)
                    if curr[src].stations:
                        i = rnd.randrange(len(curr[src].stations))
                        node = curr[src].stations.pop(i)
                        insert_pos = rnd.randrange(len(curr[dst].stations)+1)
                        curr[dst].stations.insert(insert_pos, node)

                # 중복 제거
                for ln in curr:
                    seen = set()
                    ln.stations = [s for s in ln.stations if not (s in seen or seen.add(s))]

                # 유효성 + 연결 보정
                min_len = 3
                used = set(itertools.chain.from_iterable(ln.stations for ln in curr))
                if len(used) < len(self.stations) or any(len(ln.stations) < min_len for ln in curr):
                    curr = [ln.copy() for ln in best_lines]
                    continue
                self._ensure_connectivity(curr)
                self._ensure_multi_hubs(curr, min_shared=2)

            metrics = self.evaluate(curr, sim_time=SIM_T, speed=speed, dwell_time=dwell_time, dt=dt, trains_per_line=trains_per_line)
            score = _cost(metrics)
            if score < best_score:
                best_score = score
                best_lines = [ln.copy() for ln in curr]

        return PlanResult(self, best_lines,
                          self.evaluate(best_lines, sim_time=SIM_T, speed=speed, dwell_time=dwell_time, dt=dt, trains_per_line=trains_per_line))

    # ----- 연결성 유틸 -----
    def _build_adj(self, lines: List[Line]) -> Dict[int, List[int]]:
        adj: Dict[int, List[int]] = {s.id: [] for s in self.stations}
        for ln in lines:
            for a, b in zip(ln.stations, ln.stations[1:]):
                if b not in adj[a]:
                    adj[a].append(b)
                if a not in adj[b]:
                    adj[b].append(a)
        return adj

    def _components(self, lines: List[Line]) -> List[List[int]]:
        adj = self._build_adj(lines)
        seen = set()
        comps = []
        for s in range(len(self.stations)):
            if s in seen:
                continue
            if all(s not in ln.stations for ln in lines):
                seen.add(s)
                comps.append([s])
                continue
            q = [s]
            seen.add(s)
            comp = [s]
            while q:
                u = q.pop(0)
                for v in adj.get(u, []):
                    if v not in seen:
                        seen.add(v)
                        q.append(v)
                        comp.append(v)
            comps.append(comp)
        return comps

    def _ensure_connectivity(self, lines: List[Line]) -> None:
        while True:
            comps = self._components(lines)
            all_used = set(itertools.chain.from_iterable(ln.stations for ln in lines))
            if len(all_used) < len(self.stations):
                unused = [i for i in range(len(self.stations)) if i not in all_used]
                if unused:
                    sid = unused[0]
                    best = None
                    for li, ln in enumerate(lines):
                        for pos in range(len(ln.stations)+1):
                            cand = ln.stations[:pos] + [sid] + ln.stations[pos:]
                            delta = path_length(cand, self.stations) - path_length(ln.stations, self.stations)
                            if best is None or delta < best[0]:
                                best = (delta, li, pos)
                    if best:
                        _, li, pos = best
                        lines[li].stations.insert(pos, sid)
                    continue

            used_nodes = set(itertools.chain.from_iterable(ln.stations for ln in lines))
            adj = self._build_adj(lines)
            if used_nodes:
                start = next(iter(used_nodes))
                q = [start]
                vis = {start}
                while q:
                    u = q.pop(0)
                    for v in adj.get(u, []):
                        if v in used_nodes and v not in vis:
                            vis.add(v); q.append(v)
                if vis == used_nodes:
                    break

            used_comps = []
            for comp in comps:
                if any(c in used_nodes for c in comp):
                    used_comps.append(comp)
            if len(used_comps) <= 1:
                break

            best = None
            for i in range(len(used_comps)):
                for j in range(i+1, len(used_comps)):
                    for a in used_comps[i]:
                        if a not in used_nodes:
                            continue
                        for b in used_comps[j]:
                            if b not in used_nodes:
                                continue
                            d = dist(self.stations[a], self.stations[b])
                            if best is None or d < best[0]:
                                best = (d, a, b)
            if best is None:
                break
            _, a, b = best

            host_line_idx = None
            host_pos = None
            for li, ln in enumerate(lines):
                if a in ln.stations:
                    host_line_idx = li
                    host_pos = ln.stations.index(a)
                    break
            if host_line_idx is None:
                continue
            ln = lines[host_line_idx]
            if b not in ln.stations:
                left = ln.stations[:host_pos] + [b] + ln.stations[host_pos:]
                right = ln.stations[:host_pos+1] + [b] + ln.stations[host_pos+1:]
                if path_length(left, self.stations) <= path_length(right, self.stations):
                    ln.stations = left
                else:
                    ln.stations = right

    def _insert_best(self, line: Line, sid: int) -> None:
        if sid in line.stations:
            return
        best = None
        for pos in range(len(line.stations)+1):
            cand = line.stations[:pos] + [sid] + line.stations[pos:]
            delta = path_length(cand, self.stations) - path_length(line.stations, self.stations)
            if best is None or delta < best[0]:
                best = (delta, pos)
        if best:
            line.stations.insert(best[1], sid)

    def _ensure_multi_hubs(self, lines: List[Line], min_shared: int = 2) -> None:
        m = len(lines)
        if m <= 1:
            return
        for i in range(m):
            for j in range(i+1, m):
                A, B = lines[i], lines[j]
                shared = set(A.stations) & set(B.stations)
                while len(shared) < min_shared:
                    best = None
                    for a in A.stations:
                        for b in B.stations:
                            if a == b:
                                continue
                            d = dist(self.stations[a], self.stations[b])
                            if best is None or d < best[0]:
                                best = (d, a, b)
                    if best is None:
                        break
                    _, a, b = best
                    self._insert_best(A, b)
                    self._insert_best(B, a)
                    shared = set(A.stations) & set(B.stations)


@dataclass
class PlanResult:
    planner: Planner
    lines: List[Line]
    metrics: Dict[str, float]

    def report(self, plot: bool = False, out_path: str = "DUMMY/network_plan.png", figsize=(6,6)):
        print("Best plan metrics:")
        for k, v in self.metrics.items():
            if k =="makespan":
                continue
            print(f"  {k}: {v:.3f}")
        for i, ln in enumerate(self.lines):
            print(f"Line {i+1}: {ln.stations}")
        if plot:
            self.plot_network(out_path=out_path, figsize=figsize)

    def plot_network(self, out_path: str = "DUMMY/network_plan.png", figsize=(6,6)):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("[plot_network] matplotlib이 필요합니다. `pip install matplotlib` 후 다시 시도하세요.")
            return

        stations = self.planner.stations
        xs = [s.x for s in stations]
        ys = [s.y for s in stations]

        fig, ax = plt.subplots(figsize=figsize)

        # 라인(노선) 그리기
        palette = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd",
                   "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"]
        for i, ln in enumerate(self.lines):
            color = palette[i % len(palette)]
            pts_x = [stations[sid].x for sid in ln.stations]
            pts_y = [stations[sid].y for sid in ln.stations]
            ax.plot(pts_x, pts_y, "-", linewidth=2, color=color, alpha=0.9, label=f"Line {i+1}")

        # 정거장 점 + 인덱스 라벨
        ax.scatter(xs, ys, s=30, c="black", zorder=3)
        for s in stations:
            ax.text(s.x, s.y, str(s.id), fontsize=9, ha="left", va="bottom")

        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("x"); ax.set_ylabel("y")
        ax.set_title("Mini Metro Plan (stations with indices)")
        ax.grid(True, alpha=0.25)
        ax.legend(loc="best", fontsize=8)
        fig.tight_layout()

        if out_path:
            i=0
            _path = Path(out_path).expanduser()
            basename = _path.stem
            while True:
                if not os.path.exists(out_path):
                    break
                i+=1
                out_path= os.path.join(_path.parent, basename+f"_{i}{_path.suffix}")
            fig.savefig(out_path, dpi=150)
            print(f"[plot_network] saved: {out_path}")
        plt.close(fig)


# ----------------------------
# 실행 예시
# ----------------------------
if __name__ == "__main__":
    planner = Planner.random_instance(n_stations=25, n_passengers=600, seed=42)
    best = planner.optimize(k_lines=5, iter_outer=40, iter_inner=80, trains_per_line=2,
                            speed=1.2, dwell_time=5.0, dt=0.2, seed=42)
    best.report(plot=True, out_path="DUMMY/plan.png")
