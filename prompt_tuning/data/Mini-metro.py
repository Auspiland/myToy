from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from pathlib import Path
import numpy as np
import math, heapq
from collections import defaultdict
import os
import random
import itertools
import statistics
from tqdm.auto import trange


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

# === 실행 최대 시간 ===
SIM_T = 3600.0

# === 규모별 기본 가중치 테이블 ===
BASE_WEIGHTS = {
    "small":   {"two_opt": 4, "swap": 3, "move": 2, "nearest_insertion": 1, "split_merge": 1, "long_edge_attach": 1, "line_pair_attach": 0},
    "large":   {"two_opt": 2, "swap": 1, "move": 3, "nearest_insertion": 3, "split_merge": 1, "long_edge_attach": 2, "line_pair_attach": 2},
    "default": {"two_opt": 3, "swap": 2, "move": 3, "nearest_insertion": 2, "split_merge": 1, "long_edge_attach": 2, "line_pair_attach": 1},
}

# === 단계별 보정치 테이블 ===
PHASE_ADJ = {
    "early":  {"two_opt": -1, "swap": -1, "move": 0,  "nearest_insertion": +1, "split_merge": +1, "long_edge_attach": +1, "line_pair_attach": +1},
    "mid":    {"two_opt":  0, "swap":  0, "move": 0,  "nearest_insertion":  0, "split_merge":  0, "long_edge_attach": +1, "line_pair_attach":  0},
    "late":   {"two_opt": +1, "swap": +1, "move": -1, "nearest_insertion": -1, "split_merge":  0, "long_edge_attach":  0, "line_pair_attach":  0},
}

# === COST 보정치 테이블 ===
COST_PARAMS = {
    "weight_line_length": 0.10,   # 총 선로 길이 가중치
    "weight_cross_penalty": 1.50, # 교차 패널티 계수
    "weight_hub_penalty": 1.20,   # 허브(최대 차수) 패널티 계수
    "free_cross_budget": 2,       # 교차 무상 예산
    "hub_degree_threshold": 4,    # 허브 차수 기준
}


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

def _dist_xy(stations, i, j):
    si, sj = stations[i], stations[j]
    return math.hypot(si.x - sj.x, si.y - sj.y)

def _line_length(self_obj, path):
    # path: 정거장 인덱스 리스트
    if len(path) < 2:
        return 0.0
    d = 0.0
    for a, b in zip(path, path[1:]):
        d += _dist_xy(self_obj.stations, a, b)
    return d

def compute_shortline_params(num_stations: int, k_lines: int):
    """
    반환:
      min_nodes: 라인별 최소 정거장 수(동적)
      short_bias: 짧은 라인 우선 가중치 (nearest_insertion 타깃 선택용)
      lam_short: 코스트에서 짧은 라인 패널티 가중치
    """
    N, K = max(1, num_stations), max(1, k_lines)
    avg = N / K                       # 라인당 평균 정거장 수
    base = max(3, int(round(avg * 0.55)))  # 평균의 55%를 하한으로 (최소 3)
    # 매우 큰 규모에서 과도제약 방지: 상한은 평균의 85%
    min_nodes = min(int(round(avg * 0.85)), base)

    # 타깃 가중치(짧은 라인 우선): 평균에서 얼마나 모자라는지에 비례
    # 스케일을 N,K에 덜 민감하게: 평균 대비 부족분 비율 사용
    short_bias = 1.5 if N < 60 else 1.2  # 소규모에 더 강하게

    # 코스트 가중치도 규모 무관하게 정규화
    # (라인당 평균 기준으로 제곱패널티 합을 k로 나눠 스케일 안정화)
    lam_short = 0.6 if N < 80 else 0.45

    return max(3, min_nodes), short_bias, lam_short


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
        # self._ensure_multi_hubs(lines, min_shared=2) # 모든 간선끼리 직접 연결 보장
        self._ensure_line_graph_connectivity(lines)  # 간접 연결만 보장
        return lines

    def evaluate(self, lines: List[Line], sim_time: float = 3600.0, speed: float = 1.0,
                 dwell_time: float = 5.0, dt: float = 1.0, trains_per_line: int = 1) -> Dict[str, float]:
        net = Network(self.stations, [ln.copy() for ln in lines])
        sim = Simulator(net, [Passenger(p.origin, p.dest, p.created_t) for p in self.passengers],
                        speed=speed, dwell_time=dwell_time, dt=dt, trains_per_line=trains_per_line)
        return sim.simulate(max_time=sim_time)

    def pick_move(self, rnd, t, T, N, k_lines):
        # 규모별 분류
        if N <= 30 and k_lines <= 4:
            base = BASE_WEIGHTS["small"]
        elif N > 80 or k_lines > 6:
            base = BASE_WEIGHTS["large"]
        else:
            base = BASE_WEIGHTS["default"]

        # 단계별 분류
        phase_ratio = t / max(1, T - 1)
        if phase_ratio <= 0.3:
            phase_adj = PHASE_ADJ["early"]
        elif phase_ratio <= 0.7:
            phase_adj = PHASE_ADJ["mid"]
        else:
            phase_adj = PHASE_ADJ["late"]

        # 합산 및 하한 0
        weights = {k: max(0, base[k] + phase_adj.get(k, 0)) for k in base}
        if sum(weights.values()) == 0:
            weights["two_opt"] = 1  # 최소 하나 보장

        ops = list(weights.keys())
        wts = list(weights.values())
        return rnd.choices(ops, wts, k=1)[0]

    def _m(self, m: Dict[str, float], key: str, default: float = float("inf")) -> float:
        val = m.get(key, None)
        return float(val) if val is not None else default

    def pick_best(self,
        results: List[PlanResult],
        criterion: str = "auto",           # "cost" | "makespan" | "multi" | "auto"
        weights: Optional[Dict[str, float]] = None,  # multi 모드 전용
    ) -> PlanResult:
        assert results, "results가 비어 있습니다."
        if criterion == "auto":
            criterion = "cost" if results[0].score != float("inf") else "makespan"

        if criterion == "cost":
            return min(results, key=lambda r: (r.score, self._m(r.metrics, "makespan")))
        elif criterion == "makespan":
            return min(results, key=lambda r: (self._m(r.metrics, "makespan"), r.score))
        elif criterion == "multi":
            w = {"cost": 1.0, "makespan": 0.3, "done_ratio": -0.2}
            if weights:
                w.update(weights)
            def key_fn(r: PlanResult):
                cost = r.score
                mksp = self._m(r.metrics, "makespan")
                done = float(r.metrics.get("done_ratio", 0.0))
                comp = w["cost"]*cost + w["makespan"]*mksp + w["done_ratio"]*done
                return (comp, cost, mksp, -done)
            return min(results, key=key_fn)
        else:
            raise ValueError(f"알 수 없는 criterion: {criterion}")

    def rank_results(self, results: List[PlanResult], criterion: str = "auto", topk: int = 5) -> List[PlanResult]:
        if not results:
            return []
        if criterion == "auto":
            criterion = "cost" if results[0].score != float("inf") else "makespan"
        if criterion == "cost":
            key_fn = lambda r: (r.score, self._m(r.metrics, "makespan"))
        elif criterion == "makespan":
            key_fn = lambda r: (self._m(r.metrics, "makespan"), r.score)
        elif criterion == "multi":
            key_fn = lambda r: (
                r.score + 0.3*self._m(r.metrics, "makespan") - 0.2*float(r.metrics.get("done_ratio", 0.0)),
                r.score,
                self._m(r.metrics, "makespan"),
                -float(r.metrics.get("done_ratio", 0.0)),
            )
        else:
            raise ValueError(f"알 수 없는 criterion: {criterion}")
        return sorted(results, key=key_fn)[:topk]

    def optimize_N(
        self,
        k_lines: int,
        iter_outer: int = 40,
        iter_inner: int = 60,
        speed: float = 1.0,
        dwell_time: float = 5.0,
        dt: float = 1.0,
        trains_per_line: int = 1,
        start_seed: int = 0,
        N: int = 1,
        criterion: str = "cost",      # "cost" | "makespan" | "multi" | "auto"
        weights: Optional[Dict[str, float]] = None,
        desc: str = "Multi-seed optimize",
        show_progress: bool = True,
    ) -> List[PlanResult]:
        """
        start_seed부터 N개 시드를 순회하며 self.optimize()를 실행하고 PlanResult 리스트를 반환합니다.
        PlanResult.metrics에는 'cost'가 포함되어 있어야 하며, PlanResult.score로 접근 가능합니다.
        """
        results: List[PlanResult] = []
        iterator = trange(N, desc=desc) if show_progress else range(N)

        for i in iterator:
            seed = start_seed + i
            res: PlanResult = self.optimize(
                k_lines=k_lines,
                iter_outer=iter_outer,
                iter_inner=iter_inner,
                speed=speed,
                dwell_time=dwell_time,
                dt=dt,
                trains_per_line=trains_per_line,
                seed=seed,
            )
            results.append(res)
            if show_progress:
                try:
                    val = res.score
                    mk = res.metrics.get("makespan", None)
                    postfix = {"seed": seed, "score": f"{val:.3f}"}
                    if mk is not None:
                        postfix["mksp"] = f"{mk:.3f}"
                    iterator.set_postfix(postfix)
                except Exception:
                    iterator.set_postfix({"seed": seed})
        return self.pick_best(results, criterion=criterion, weights=weights)

    # 로컬 서치
    def optimize(self, k_lines: int, iter_outer: int = 40, iter_inner: int = 60,
                 speed: float = 1.0, dwell_time: float = 5.0, dt: float = 1.0,
                 trains_per_line: int = 1, seed: int = 0) -> 'PlanResult':
        rnd = random.Random(seed)
        lines = self.initial_lines(k_lines, seed=seed)
        best_lines = [ln.copy() for ln in lines]
        LINE_MIN_NODES, SHORT_TARGET_BIAS, LAM_SHORT = compute_shortline_params(len(self.stations), k_lines)


        # def _cost(metrics):
        #     return metrics["makespan"] + (1.0 - metrics["done_ratio"]) * SIM_T * 1000.0

        def _cost(lines, metrics):

            pts = np.array([(s.x, s.y) for s in self.stations], float)

            # ---------- 기존 지표 ----------
            def total_length():
                L = 0.0
                for ln in lines:
                    for a, b in zip(ln.stations, ln.stations[1:]):
                        L += np.linalg.norm(pts[a] - pts[b])
                return L

            def line_crossings():
                def ccw(a, b, c):
                    a3 = np.append(a, 0); b3 = np.append(b, 0); c3 = np.append(c, 0)
                    return np.cross(b3 - a3, c3 - a3)[2]  # z축
                def seg_intersect(p1, p2, p3, p4):
                    ab1, ab2 = ccw(p1,p2,p3), ccw(p1,p2,p4)
                    cd1, cd2 = ccw(p3,p4,p1), ccw(p3,p4,p2)
                    return (ab1*ab2 < 0) and (cd1*cd2 < 0)

                segs = []
                for ln in lines:
                    for a,b in zip(ln.stations, ln.stations[1:]):
                        segs.append((a,b))
                cnt = 0
                for i in range(len(segs)):
                    a,b = segs[i]; p1,p2 = pts[a], pts[b]
                    for j in range(i+1, len(segs)):
                        c,d = segs[j]
                        if len({a,b,c,d}) < 4:  # 공유 노드는 교차로 보지 않음
                            continue
                        if seg_intersect(p1,p2,pts[c],pts[d]):
                            cnt += 1
                return cnt

            def max_station_degree():
                deg = [0]*len(self.stations)
                for ln in lines:
                    for a,b in zip(ln.stations, ln.stations[1:]):
                        deg[a]+=1; deg[b]+=1
                return max(deg) if deg else 0

            def shortline_penalty():
                pen = 0.0
                for ln in lines:
                    deficit = max(0, LINE_MIN_NODES - len(ln.stations))
                    pen += deficit * deficit
                return pen / max(1, len(lines))

            # ---------- detour(우회율) 패널티 ----------
            # 그래프: 노선의 인접 역을 undirected로 연결. 가중치는 "거리" 기준(시간을 쓰려면 속도/정차시간 반영 가능).
            def build_graph():
                graph = defaultdict(list)
                for ln in lines:
                    st = ln.stations
                    for a, b in zip(st, st[1:]):
                        w = float(np.linalg.norm(pts[a] - pts[b]))
                        graph[a].append((b, w))
                        graph[b].append((a, w))
                return graph

            def dijkstra(graph, start):
                INF = float('inf')
                dist = [INF]*len(self.stations)
                dist[start] = 0.0
                pq = [(0.0, start)]
                while pq:
                    d,u = heapq.heappop(pq)
                    if d != dist[u]:
                        continue
                    for v,w in graph[u]:
                        nd = d + w
                        if nd < dist[v]:
                            dist[v] = nd
                            heapq.heappush(pq, (nd, v))
                return dist  # list[float]

            def compute_detour_penalty():
                # ---- 파라미터(필요 시 COST_PARAMS로 외부화) ----
                detour_tau     = COST_PARAMS.get("detour_tau", 1.8)     # 허용 우회율
                detour_p       = COST_PARAMS.get("detour_p", 1.5)       # 곡률
                detour_top_q   = COST_PARAMS.get("detour_top_q", None)  # 상위 q%만 벌점(예: 0.1). None이면 평균
                od_cap         = COST_PARAMS.get("detour_od_cap", 400)  # 계산량 제한

                # OD 집합 구성: (o, z, demand)
                od_list = []
                if hasattr(self, "passengers") and self.passengers:
                    # self.passengers가 (origin_id, dest_id, demand) 형태라고 가정
                    for p in self.passengers:
                        o, z = int(p.origin), int(p.dest)
                        if o == z: 
                            continue
                        demand = float(getattr(p, "demand", 1.0))
                        od_list.append((o, z, demand))
                else:
                    # 승객 정보가 없으면 역 쌍을 샘플링
                    n = len(self.stations)
                    if n <= 1:
                        return 0.0
                    # 격자 샘플링: 먼 쌍이 어느 정도 포함되게 간단 샘플
                    idx = np.arange(n)
                    # 고르게 섞은 뒤 앞에서 일부만 사용
                    rng = np.random.default_rng(12345)
                    rng.shuffle(idx)
                    pairs = []
                    for i in range(min(n, 64)):  # 최대 64개 원점
                        o = int(idx[i])
                        # o와 충분히 떨어진 후보를 몇 개 선택
                        cand = rng.choice(idx, size=6, replace=False)
                        for z in cand:
                            z = int(z)
                            if o == z:
                                continue
                            pairs.append((o, z, 1.0))
                    od_list = pairs[:od_cap]

                if not od_list:
                    return 0.0

                graph = build_graph()

                # 출발역별로 Dijkstra 1회
                origins = sorted(set(o for (o, _, _) in od_list))
                dist_cache = {o: dijkstra(graph, o) for o in origins}

                # detour 계산
                terms = []  # (over^p, weight)
                for (o, z, demand) in od_list:
                    direct = float(np.linalg.norm(pts[o] - pts[z]))
                    if direct == 0.0:
                        continue
                    net = dist_cache[o][z]
                    if math.isinf(net):
                        # 연결 안되어 있으면 큰 벌점(직선 대비 무한) → over=∞ 처리 대신 큰 상수로 clamp
                        over_p = (10.0)**detour_p  # 필요시 조정
                    else:
                        stretch = net / direct
                        over = max(0.0, stretch - detour_tau)
                        over_p = over ** detour_p
                    w = float(demand) if demand is not None else 1.0
                    terms.append((over_p, w))

                if not terms:
                    return 0.0

                # 상위 q%만 쓰는 옵션(극단적 우회만 잡고 싶을 때)
                if detour_top_q is not None and 0.0 < detour_top_q < 1.0:
                    xs = sorted((t[0] for t in terms), reverse=True)
                    k = max(1, int(len(xs) * detour_top_q))
                    sel = xs[:k]
                    penalty = float(np.mean(sel))
                else:
                    num = sum(w for _, w in terms)
                    if num <= 0:
                        penalty = float(np.mean([t for t,_ in terms]))
                    else:
                        penalty = sum(v*w for v,w in terms) / num
                return penalty

            # ---------- 기존 비용 합산 ----------
            L  = total_length()
            X  = line_crossings()
            H  = max_station_degree()

            lam_len   = COST_PARAMS["weight_line_length"]
            lam_cross = COST_PARAMS["weight_cross_penalty"]
            lam_hub   = COST_PARAMS["weight_hub_penalty"]
            C0        = COST_PARAMS["free_cross_budget"]
            D0        = COST_PARAMS["hub_degree_threshold"]

            penalty_cross = lam_cross * max(0, X - C0) ** 2
            penalty_hub   = lam_hub   * max(0, H - D0) ** 2
            SL = shortline_penalty()
            lam_short = LAM_SHORT

            # ---- detour 패널티 결합 ----
            detour_pen = compute_detour_penalty()
            lam_detour = COST_PARAMS.get("weight_detour_penalty", 0.5)

            return (
                metrics["makespan"]
                + (1.0 - metrics["done_ratio"]) * SIM_T * 1000.0
                + lam_len * L
                + penalty_cross
                + penalty_hub
                + lam_short * SL
                + lam_detour * detour_pen
            )

        best_metrics = self.evaluate(best_lines, sim_time=SIM_T, speed=speed, dwell_time=dwell_time, dt=dt, trains_per_line=trains_per_line)
        best_score = _cost(best_lines, best_metrics)

        for outer in range(iter_outer):
            curr = [ln.copy() for ln in best_lines]
            for _ in range(iter_inner):
                move_type = self.pick_move(rnd, outer, iter_outer, len(self.stations), k_lines)
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
                    # 하이퍼(상단 전역 또는 클래스 파라미터로 둬도 됩니다)
                    LINE_MIN_NODES = max(3, getattr(self, "line_min_nodes", 3))
                    SHORT_TARGET_BIAS = getattr(self, "short_target_bias", 1.5)

                    # 1) 소스 라인/정거장 선택: 짧은 라인(L<=min)에서는 pop 금지, 정거장은 기하평균 가중
                    src_lines = [li for li, ln in enumerate(curr) if len(ln.stations) > LINE_MIN_NODES]
                    if not src_lines:
                        continue
                    li = rnd.choice(src_lines)
                    st = curr[li].stations
                    if len(st) == 0:
                        continue
                    def w_station(idx):
                        if len(st) == 1: return 0.0
                        if idx == 0:     return _dist_xy(self.stations, st[0], st[1])
                        if idx == len(st)-1: return _dist_xy(self.stations, st[-2], st[-1])
                        dl = _dist_xy(self.stations, st[idx-1], st[idx])
                        dr = _dist_xy(self.stations, st[idx],   st[idx+1])
                        return (dl * dr) ** 0.5
                    idx = rnd.choices(range(len(st)), weights=[max(1e-6, w_station(i)) for i in range(len(st))], k=1)[0]
                    node = st.pop(idx)

                    # 2) 타깃 라인 선택: 짧은 라인일수록 가중 ↑ (부족비율 기반)
                    tgt_list = [tj for tj in range(len(curr)) if tj != li]
                    if not tgt_list:
                        st.insert(idx, node); continue
                    def w_line(tj):
                        L = len(curr[tj].stations)
                        deficit = max(0, LINE_MIN_NODES - L) / max(1, LINE_MIN_NODES)
                        return 1.0 + SHORT_TARGET_BIAS * deficit
                    tj = rnd.choices(tgt_list, weights=[w_line(t) for t in tgt_list], k=1)[0]
                    tp = curr[tj].stations

                    # 3) 이미 있으면 복원, 아니면 Δ길이 최소 위치에 삽입
                    if node in tp:
                        st.insert(idx, node)
                    else:
                        if len(tp) == 0:
                            tp.append(node)
                        elif len(tp) == 1:
                            if _dist_xy(self.stations, node, tp[0]) <= _dist_xy(self.stations, tp[0], node):
                                tp.insert(0, node)
                            else:
                                tp.append(node)
                        else:
                            best_pos, best_delta = 0, float("inf")
                            for k in range(len(tp)-1):
                                u, v = tp[k], tp[k+1]
                                d = (_dist_xy(self.stations, u, node)
                                    + _dist_xy(self.stations, node, v)
                                    - _dist_xy(self.stations, u, v))
                                if d < best_delta: best_delta, best_pos = d, k+1
                            df = _dist_xy(self.stations, node, tp[0])
                            db = _dist_xy(self.stations, tp[-1], node)
                            insert_pos = 0 if df < min(best_delta, db) else (len(tp) if db < min(best_delta, df) else best_pos)
                            tp.insert(insert_pos, node)


                elif move_type == "split_merge" and len(curr) >= 3:
                    # 각 라인의 길이 계산
                    lengths = []
                    for li, ln in enumerate(curr):
                        L = _line_length(self, ln.stations)
                        lengths.append((L, li))
                    if not lengths:
                        pass
                    else:
                        # 가장 긴 A, 가장 짧은 두 개 B, C
                        lengths_sorted = sorted(lengths)           # 오름차순
                        (La, ai) = max(lengths, key=lambda x: x[0])  # 가장 긴
                        # 가장 짧은 두 개
                        bi = lengths_sorted[0][1]
                        # C 후보는 bi와 다른 것 중 가장 짧은 것
                        ci = None
                        for L, li in lengths_sorted[1:]:
                            if li != bi:
                                ci = li
                                break
                        if ci is None or ai in (bi, ci):
                            # 라인 수가 적거나 특이 케이스면 스킵
                            pass
                        else:
                            A = curr[ai].stations
                            B = curr[bi].stations
                            C = curr[ci].stations
                            if len(A) >= 6:
                                # A를 두 동강 (안정적 범위: [2, len-2)에서 컷)
                                cut = random.randrange(2, len(A) - 2)
                                A1, A2 = A[:cut], A[cut:]

                                # B와 C를 합쳐 하나의 라인으로
                                BC = B + C

                                # k_lines 유지: A←A1, B←BC, C←A2 로 재배치
                                curr[ai].stations = A1
                                curr[bi].stations = BC
                                curr[ci].stations = A2
                
                elif move_type == "nearest_insertion" and len(curr) >= 2:
                    # === 소스 정거장 선택: 양쪽 연결(인접 간선) 길이 합에 비례해 가중 랜덤 선택 ===
                    candidates = []   # (src_line_idx, station_idx)
                    weights = []      # 양쪽(또는 한쪽) 인접 간선 길이 합

                    for li, ln in enumerate(curr):
                        st = ln.stations
                        n = len(st)
                        if n == 0:
                            continue
                        for idx in range(n):
                            if n == 1:
                                w = 0.0
                            elif idx == 0:
                                w = _dist_xy(self.stations, st[0], st[1])
                            elif idx == n - 1:
                                w = _dist_xy(self.stations, st[n - 2], st[n - 1])
                            else:
                                dl = _dist_xy(self.stations, st[idx - 1], st[idx])
                                dr = _dist_xy(self.stations, st[idx], st[idx + 1])
                                w = math.sqrt(dl**2 + dr**2)
                            candidates.append((li, idx))
                            weights.append(max(1e-6, w))  # 가중치 0 방지

                    if not candidates:
                        continue  # 소스가 없으면 이번 변이는 스킵

                    src, i = rnd.choices(candidates, weights=weights, k=1)[0]
                    s = curr[src].stations.pop(i)  # s 제거

                    # === 타깃 라인 선택: '짧은 라인'일수록 가중 ↑ ===
                    tgt_candidates = [idx for idx in range(len(curr)) if idx != src]
                    if not tgt_candidates:
                        curr[src].stations.insert(i, s)  # 복원
                    else:
                        t_weights = []
                        for idx in tgt_candidates:
                            tp = curr[idx].stations
                            deficit = max(0, LINE_MIN_NODES - len(tp))  # 짧을수록 큼
                            deficit_ratio = deficit / max(1, LINE_MIN_NODES)
                            t_weights.append(1.0 + SHORT_TARGET_BIAS * deficit_ratio)
                        tgt = rnd.choices(tgt_candidates, weights=t_weights, k=1)[0]
                        tp = curr[tgt].stations

                        # 중복 방지
                        if s in tp:
                            curr[src].stations.insert(i, s)
                        else:
                            # Δ = d(u,s)+d(s,v)-d(u,v) 최소인 위치 찾기
                            if len(tp) == 0:
                                tp.append(s)
                            elif len(tp) == 1:
                                if _dist_xy(self.stations, s, tp[0]) <= _dist_xy(self.stations, tp[0], s):
                                    tp.insert(0, s)
                                else:
                                    tp.append(s)
                            else:
                                best_pos = 0
                                best_delta = float("inf")
                                for k in range(len(tp) - 1):
                                    u, v = tp[k], tp[k + 1]
                                    delta = (
                                        _dist_xy(self.stations, u, s)
                                        + _dist_xy(self.stations, s, v)
                                        - _dist_xy(self.stations, u, v)
                                    )
                                    if delta < best_delta:
                                        best_delta = delta
                                        best_pos = k + 1
                                # 양 끝 비교
                                delta_front = _dist_xy(self.stations, s, tp[0])
                                delta_back  = _dist_xy(self.stations, tp[-1], s)
                                best_choice = ("mid", best_pos, best_delta)
                                if delta_front < best_choice[2]:
                                    best_choice = ("front", 0, delta_front)
                                if delta_back < best_choice[2]:
                                    best_choice = ("back", len(tp), delta_back)
                                tp.insert(best_choice[1], s)

                elif move_type == "long_edge_attach":
                    # 1) 가장 긴 간선 찾기
                    edges = []  # (length, line_idx, seg_idx, u, v)
                    for li, ln in enumerate(curr):
                        st = ln.stations
                        for k in range(len(st)-1):
                            u, v = st[k], st[k+1]
                            L = _dist_xy(self.stations, u, v)
                            edges.append((L, li, k, u, v))
                    if not edges:
                        pass
                    else:
                        edges.sort(reverse=True)
                        Lmax, li, k, u, v = edges[0]
                        base_len = Lmax

                        # 2) 후보 계산: (A) 엔드포인트 이동, (B) 다리 삽입
                        best_action = None   # ("rewire", delta, params...) or ("bridge", delta, params...)

                        # --- (A) 엔드포인트 이동(rewire) ---
                        for move_node in (u, v):
                            # 원 라인에서 제거 후 타깃 라인에 최소증가 삽입
                            path = curr[li].stations
                            if move_node not in path: 
                                continue
                            rem_idx = path.index(move_node)
                            # 임시 제거
                            popped = path.pop(rem_idx)

                            # 타깃 라인 후보: 자기 라인 제외
                            candidates = [idx for idx in range(len(curr)) if idx != li]
                            if candidates:
                                best_delta, best_tgt, best_pos = float("inf"), None, None
                                for tgt in candidates:
                                    tp = curr[tgt].stations
                                    if popped in tp:
                                        continue  # 중복 방지(의도적으로 공유하고 싶다면 제거)
                                    if len(tp) == 0:
                                        delta = 0.0  # 그냥 추가
                                        pos = 0
                                    elif len(tp) == 1:
                                        # 앞/뒤 중 더 짧은 쪽
                                        d0 = _dist_xy(self.stations, popped, tp[0])
                                        delta = d0
                                        pos = 0 if d0 <= d0 else 1
                                    else:
                                        # 간선 사이 삽입의 최소 증가 길이
                                        best_pos_t, best_d_t = 0, float("inf")
                                        for kk in range(len(tp)-1):
                                            a, b = tp[kk], tp[kk+1]
                                            d = (_dist_xy(self.stations, a, popped)
                                                + _dist_xy(self.stations, popped, b)
                                                - _dist_xy(self.stations, a, b))
                                            if d < best_d_t:
                                                best_d_t, best_pos_t = d, kk+1
                                        # 양끝 비교
                                        df = _dist_xy(self.stations, popped, tp[0])
                                        db = _dist_xy(self.stations, popped, tp[-1])
                                        delta = best_d_t
                                        pos = best_pos_t
                                        if df < delta:
                                            delta, pos = df, 0
                                        if db < delta:
                                            delta, pos = db, len(tp)
                                    if delta < best_delta:
                                        best_delta, best_tgt, best_pos = delta, tgt, pos
                                if best_tgt is not None:
                                    # 엔드포인트 이동으로 생기는 "원 라인 길이 변화"도 반영해야 엄밀하지만,
                                    # 긴 간선 끝점 제거 자체가 대체로 길이 단축 방향이라 간단화(원 라인 길이 감소 ≈ base_len/2 이상 기대)
                                    # 비교 용도이므로 delta만 사용
                                    if best_action is None or ("rewire" == best_action[0] and best_delta < best_action[1]) or ("bridge" == best_action[0] and best_delta < best_action[1]):
                                        best_action = ("rewire", best_delta, move_node, li, best_tgt, best_pos)

                            # 복구
                            path.insert(rem_idx, popped)

                        # --- (B) 다리 삽입(bridge) ---
                        best_delta_b, best_w = float("inf"), None
                        for lj, ln in enumerate(curr):
                            if lj == li: 
                                continue
                            for w in ln.stations:
                                delta = (_dist_xy(self.stations, u, w)
                                        + _dist_xy(self.stations, w, v)
                                        - base_len)
                                if delta < best_delta_b:
                                    best_delta_b, best_w = delta, w
                        if best_w is not None:
                            if best_action is None or best_delta_b < best_action[1]:
                                best_action = ("bridge", best_delta_b, li, k, best_w)

                        # 3) 실행: 개선폭(Δ)이 더 큰 한 가지 액션만 수행
                        if best_action is not None:
                            if best_action[0] == "rewire":
                                _, _, node, src_li, tgt_li, pos = best_action
                                # 원 라인에서 제거
                                p = curr[src_li].stations
                                if node in p:
                                    p.remove(node)
                                # 타깃 라인에 삽입
                                tp = curr[tgt_li].stations
                                if node not in tp:
                                    tp.insert(pos, node)
                            else:  # "bridge"
                                _, _, li2, k2, w = best_action
                                path = curr[li2].stations
                                if w not in path:
                                    path.insert(k2+1, w)

                elif move_type == "line_pair_attach" and len(curr) >= 2:
                    # 두 노선이 서로 정거장을 공유하지 않으면서 공간적으로 가장 가까운 쌍을 찾는다.

                    def best_insert_pos(tp, node):
                        # 타깃 라인 tp에 node를 넣을 때 길이 증가가 최소인 위치와 증가량을 반환
                        if len(tp) == 0:
                            return (0.0, 0)
                        if len(tp) == 1:
                            d = _dist_xy(self.stations, node, tp[0])
                            return (d, 0)
                        best_pos, best_delta = 0, float("inf")
                        for kk in range(len(tp) - 1):
                            a, b = tp[kk], tp[kk + 1]
                            d = (_dist_xy(self.stations, a, node)
                                + _dist_xy(self.stations, node, b)
                                - _dist_xy(self.stations, a, b))
                            if d < best_delta:
                                best_delta, best_pos = d, kk + 1
                        df = _dist_xy(self.stations, node, tp[0])
                        db = _dist_xy(self.stations, node, tp[-1])
                        if df < best_delta and df <= db:
                            return (df, 0)
                        if db < best_delta and db < df:
                            return (db, len(tp))
                        return (best_delta, best_pos)

                    # (1) 후보 라인 쌍 수집
                    line_sets = [set(ln.stations) for ln in curr]
                    best_pair = None  # (min_dist, a, b, sa, sb)
                    for a in range(len(curr)):
                        for b in range(a + 1, len(curr)):
                            # 이미 공유 정거장이 있으면 스킵(직접 연결됨)
                            if line_sets[a] & line_sets[b]:
                                continue
                            # 두 라인 사이 최단 정거장 쌍 찾기
                            min_d, sa, sb = float("inf"), None, None
                            for u in line_sets[a]:
                                for v in line_sets[b]:
                                    d = _dist_xy(self.stations, u, v)
                                    if d < min_d:
                                        min_d, sa, sb = d, u, v
                            if sa is not None and sb is not None:
                                if (best_pair is None) or (min_d < best_pair[0]):
                                    best_pair = (min_d, a, b, sa, sb)

                    if best_pair is None:
                        # 붙일 후보가 없음
                        pass
                    else:
                        _, a, b, sa, sb = best_pair
                        A, B = curr[a].stations, curr[b].stations

                        # (2) 어느 쪽을 공유할지 결정: sa를 B에 넣는 경우 vs sb를 A에 넣는 경우 중 Δ가 작은 쪽
                        #    (둘 다 원 라인에서는 제거하지 않음 = '공유'로 붙임)
                        if sa in B and sb in A:
                            pass  # 이미 양방향 공유가 생겼다면 할 일 없음
                        else:
                            best_action = None  # ("A<-sb", delta, pos) or ("B<-sa", delta, pos)

                            if sa not in B:
                                delta_b, pos_b = best_insert_pos(B, sa)
                                best_action = ("B<-sa", delta_b, pos_b)

                            if sb not in A:
                                delta_a, pos_a = best_insert_pos(A, sb)
                                if (best_action is None) or (delta_a < best_action[1]):
                                    best_action = ("A<-sb", delta_a, pos_a)

                            # (3) 실행: 길이 증가가 더 작은 한 쪽만 수행(조심스럽게 한 번에 한 개의 공유점만 만든다)
                            if best_action is not None:
                                kind, _, pos = best_action
                                if kind == "B<-sa" and sa not in B:
                                    B.insert(pos, sa)
                                elif kind == "A<-sb" and sb not in A:
                                    A.insert(pos, sb)


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
            # self._ensure_multi_hubs(curr, min_shared=2)  # 모든 간선끼리 직접 연결 보장
            self._ensure_line_graph_connectivity(curr)  # 간접 연결만 보장

            metrics = self.evaluate(curr, sim_time=SIM_T, speed=speed, dwell_time=dwell_time, dt=dt, trains_per_line=trains_per_line)
            score = _cost(curr, metrics)
            if score < best_score:
                best_score = score
                best_lines = [ln.copy() for ln in curr]

        return PlanResult(self, best_lines, best_score,
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

    def _ensure_line_graph_connectivity(self, lines):
        """
        각 라인을 정점으로 보고, '공통 정거장을 1개 이상 공유하면' 간선을 두는 라인 그래프를 만든 뒤
        라인 그래프가 연결되도록 최소한의 공유 정거장을 만들어 준다.
        (== 모든 라인이 하나의 컴포넌트로 연결되면 OK. 모든 쌍이 직접 만날 필요 없음.)
        """
        import math

        def dist_idx(i, j):
            si, sj = self.stations[i], self.stations[j]
            return math.hypot(si.x - sj.x, si.y - sj.y)

        # 라인별 정거장 집합
        S = [set(ln.stations) for ln in lines]
        L = len(lines)
        if L <= 1:
            return

        # 라인 그래프 인접 리스트(공통 정거장 1개 이상이면 연결)
        adj = [[] for _ in range(L)]
        for a in range(L):
            for b in range(a+1, L):
                if S[a] & S[b]:
                    adj[a].append(b)
                    adj[b].append(a)

        # 컴포넌트 분해
        comp_id = [-1]*L
        cid = 0
        for i in range(L):
            if comp_id[i] != -1: continue
            stack = [i]
            comp_id[i] = cid
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if comp_id[v] == -1:
                        comp_id[v] = cid
                        stack.append(v)
            cid += 1

        if cid == 1:
            return  # 이미 라인 그래프 연결

        # 여러 컴포넌트라면, 가까운 라인 쌍을 골라 '정거장 하나를 공유'하도록 삽입(Nearest Insertion)
        # 간단히: 기준 컴포넌트(0)에 나머지 컴포넌트를 순차적으로 붙여감
        base_comp = 0
        while True:
            comps = {}
            for li, c in enumerate(comp_id):
                comps.setdefault(c, []).append(li)
            if len(comps) == 1:
                break

            A = comps[base_comp]                   # 기준 컴포넌트 라인들
            Bc = [c for c in comps.keys() if c != base_comp][0]  # 붙일 대상 컴포넌트 하나
            B = comps[Bc]

            # (a ∈ A, b ∈ B) 중 '최단 정거장 쌍' 찾기
            best = None
            for a in A:
                for b in B:
                    # a 라인의 정거장 s, b 라인의 정거장 t 중 가장 가까운 한 쌍 (s,t)
                    for s in S[a]:
                        for t in S[b]:
                            d = dist_idx(s, t)
                            if (best is None) or (d < best[0]):
                                best = (d, a, b, s, t)
            if best is None:
                break
            _, a, b, s, t = best

            # '공유 정거장' 만들기: b 라인에 s를 삽입(= a,b가 정거장 s를 공유)
            tp = lines[b].stations
            if s not in S[b]:
                # 최소 증가 길이 위치로 삽입
                if len(tp) <= 1:
                    # 비거나 1개면 앞/뒤 아무 데나
                    insert_pos = 0 if not tp else (0 if dist_idx(s, tp[0]) <= dist_idx(tp[0], s) else 1)
                else:
                    best_pos, best_delta = 0, float("inf")
                    for k in range(len(tp)-1):
                        u, v = tp[k], tp[k+1]
                        delta = dist_idx(u, s) + dist_idx(s, v) - dist_idx(u, v)
                        if delta < best_delta:
                            best_delta, best_pos = delta, k+1
                    # 양끝 비교
                    delta_front = dist_idx(s, tp[0])
                    delta_back  = dist_idx(tp[-1], s)
                    if delta_front < best_delta and delta_front <= delta_back:
                        insert_pos = 0
                    elif delta_back < best_delta and delta_back < delta_front:
                        insert_pos = len(tp)
                    else:
                        insert_pos = best_pos
                tp.insert(insert_pos, s)
                S[b].add(s)

            # 라인 그래프 갱신(이제 a-b 연결)
            adj[a].append(b); adj[b].append(a)
            # 컴포넌트 병합: b가 속한 컴포넌트를 base_comp로 흡수
            old = comp_id[b]
            for i in range(L):
                if comp_id[i] == old:
                    comp_id[i] = base_comp


@dataclass
class PlanResult:
    planner: Planner
    lines: List[Line]
    score: float
    metrics: Dict[str, float]

    def report(self, plot: bool = False, out_path: str = "DUMMY/network_plan.png", figsize=(6,6)):
        print("Best plan metrics:")
        for k, v in self.metrics.items():
            # if k =="makespan":
            #     continue
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

    # criterion : "cost" | "makespan" | "multi" | "auto"
    weights = {"cost": 1.0, "makespan": 0.5, "done_ratio": -0.5}

    planner = Planner.random_instance(n_stations=40, n_passengers=800, seed=41)
    best = planner.optimize_N(k_lines=5, iter_outer=80, iter_inner=120, trains_per_line=3,
                            speed=1.2, dwell_time=3.0, dt=0.2, start_seed=20, N=5,
                            criterion="multi", weights=weights)
    best.report(plot=True, out_path="DUMMY/metro_graph/plan.png")
