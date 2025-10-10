# -*- coding: utf-8 -*-
"""
Network Flow algorithms: Dinic's algorithm, Min-Cost Max-Flow
"""

from collections import deque
from typing import List, Tuple, Optional
import heapq

class Edge:
    """Edge for flow networks"""
    def __init__(self, to: int, capacity: int, cost: int = 0, rev: int = 0):
        self.to = to
        self.capacity = capacity
        self.cost = cost
        self.rev = rev  # Index of reverse edge

class Dinic:
    """
    Dinic's algorithm for maximum flow
    Time: O(V^2 * E) general, O(E * sqrt(V)) for unit capacity
    """
    def __init__(self, n: int):
        self.n = n
        self.graph = [[] for _ in range(n)]
    
    def add_edge(self, from_node: int, to_node: int, capacity: int):
        """
        Add edge to flow network
        
        Args:
            from_node: Source vertex of edge
            to_node: Destination vertex of edge
            capacity: Capacity of edge
        """
        self.graph[from_node].append(Edge(to_node, capacity, 0, len(self.graph[to_node])))
        self.graph[to_node].append(Edge(from_node, 0, 0, len(self.graph[from_node]) - 1))
    
    def bfs(self, source: int, sink: int) -> bool:
        """BFS to build level graph"""
        self.level = [-1] * self.n
        self.level[source] = 0
        queue = deque([source])
        
        while queue:
            v = queue.popleft()
            for edge in self.graph[v]:
                if edge.capacity > 0 and self.level[edge.to] < 0:
                    self.level[edge.to] = self.level[v] + 1
                    queue.append(edge.to)
        
        return self.level[sink] >= 0
    
    def dfs(self, v: int, sink: int, flow: int) -> int:
        """DFS to find blocking flow"""
        if v == sink:
            return flow
        
        for i in range(self.iter[v], len(self.graph[v])):
            edge = self.graph[v][i]
            if edge.capacity > 0 and self.level[v] < self.level[edge.to]:
                d = self.dfs(edge.to, sink, min(flow, edge.capacity))
                if d > 0:
                    edge.capacity -= d
                    self.graph[edge.to][edge.rev].capacity += d
                    return d
            self.iter[v] += 1
        
        return 0
    
    def max_flow(self, source: int, sink: int) -> int:
        """
        Find maximum flow from source to sink
        
        Args:
            source: Source vertex
            sink: Sink vertex
            
        Returns:
            Maximum flow value
        """
        flow = 0
        
        while self.bfs(source, sink):
            self.iter = [0] * self.n
            f = self.dfs(source, sink, float('inf'))
            while f > 0:
                flow += f
                f = self.dfs(source, sink, float('inf'))
        
        return flow

class MCMF:
    """
    Min-Cost Max-Flow using SPFA
    """
    def __init__(self, n: int):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.INF = float('inf')
    
    def add_edge(self, from_node: int, to_node: int, capacity: int, cost: int):
        """
        Add edge to flow network with cost
        
        Args:
            from_node: Source vertex of edge
            to_node: Destination vertex of edge
            capacity: Capacity of edge
            cost: Cost per unit flow
        """
        self.graph[from_node].append(Edge(to_node, capacity, cost, len(self.graph[to_node])))
        self.graph[to_node].append(Edge(from_node, 0, -cost, len(self.graph[from_node]) - 1))
    
    def spfa(self, source: int, sink: int) -> bool:
        """SPFA to find shortest path in residual graph"""
        self.dist = [self.INF] * self.n
        self.parent = [-1] * self.n
        self.parent_edge = [-1] * self.n
        self.in_queue = [False] * self.n
        
        self.dist[source] = 0
        queue = deque([source])
        self.in_queue[source] = True
        
        while queue:
            v = queue.popleft()
            self.in_queue[v] = False
            
            for i, edge in enumerate(self.graph[v]):
                if edge.capacity > 0 and self.dist[v] + edge.cost < self.dist[edge.to]:
                    self.dist[edge.to] = self.dist[v] + edge.cost
                    self.parent[edge.to] = v
                    self.parent_edge[edge.to] = i
                    
                    if not self.in_queue[edge.to]:
                        queue.append(edge.to)
                        self.in_queue[edge.to] = True
        
        return self.dist[sink] != self.INF
    
    def min_cost_max_flow(self, source: int, sink: int) -> Tuple[int, int]:
        """
        Find minimum cost maximum flow
        
        Args:
            source: Source vertex
            sink: Sink vertex
            
        Returns:
            (max_flow, min_cost) tuple
        """
        max_flow = 0
        min_cost = 0
        
        while self.spfa(source, sink):
            # Find minimum capacity along the path
            flow = self.INF
            v = sink
            
            while v != source:
                edge = self.graph[self.parent[v]][self.parent_edge[v]]
                flow = min(flow, edge.capacity)
                v = self.parent[v]
            
            # Update capacities and cost
            v = sink
            while v != source:
                edge_idx = self.parent_edge[v]
                edge = self.graph[self.parent[v]][edge_idx]
                edge.capacity -= flow
                self.graph[v][edge.rev].capacity += flow
                v = self.parent[v]
            
            max_flow += flow
            min_cost += flow * self.dist[sink]
        
        return max_flow, min_cost

def bipartite_matching(left_size: int, right_size: int, 
                      edges: List[Tuple[int, int]]) -> int:
    """
    Find maximum bipartite matching using flow
    
    Args:
        left_size: Number of vertices in left partition
        right_size: Number of vertices in right partition
        edges: List of (left_vertex, right_vertex) edges
        
    Returns:
        Size of maximum matching
        
    Time: O(V * E)
    """
    # Create flow network: source -> left -> right -> sink
    n = left_size + right_size + 2
    source = 0
    sink = n - 1
    
    dinic = Dinic(n)
    
    # Add edges from source to left vertices
    for i in range(1, left_size + 1):
        dinic.add_edge(source, i, 1)
    
    # Add edges from left to right vertices
    for left, right in edges:
        dinic.add_edge(left, left_size + right, 1)
    
    # Add edges from right vertices to sink
    for i in range(left_size + 1, left_size + right_size + 1):
        dinic.add_edge(i, sink, 1)
    
    return dinic.max_flow(source, sink)

def min_vertex_cover_bipartite(left_size: int, right_size: int,
                              edges: List[Tuple[int, int]]) -> List[int]:
    """
    Find minimum vertex cover in bipartite graph
    
    Args:
        left_size: Number of vertices in left partition
        right_size: Number of vertices in right partition  
        edges: List of (left_vertex, right_vertex) edges
        
    Returns:
        List of vertices in minimum vertex cover
        
    Time: O(V * E)
    """
    # Use König's theorem: min vertex cover = max matching in bipartite graph
    n = left_size + right_size + 2
    source = 0
    sink = n - 1
    
    dinic = Dinic(n)
    
    # Build flow network
    for i in range(1, left_size + 1):
        dinic.add_edge(source, i, 1)
    
    for left, right in edges:
        dinic.add_edge(left, left_size + right, 1)
    
    for i in range(left_size + 1, left_size + right_size + 1):
        dinic.add_edge(i, sink, 1)
    
    # Find maximum flow
    max_flow = dinic.max_flow(source, sink)
    
    # Find minimum cut = minimum vertex cover
    visited = [False] * n
    queue = deque([source])
    visited[source] = True
    
    while queue:
        v = queue.popleft()
        for edge in dinic.graph[v]:
            if edge.capacity > 0 and not visited[edge.to]:
                visited[edge.to] = True
                queue.append(edge.to)
    
    vertex_cover = []
    
    # Add left vertices not reachable from source
    for i in range(1, left_size + 1):
        if not visited[i]:
            vertex_cover.append(i)
    
    # Add right vertices reachable from source
    for i in range(left_size + 1, left_size + right_size + 1):
        if visited[i]:
            vertex_cover.append(i)
    
    return vertex_cover