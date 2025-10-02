# -*- coding: utf-8 -*-
"""
Shortest path algorithms: Dijkstra, Floyd-Warshall, etc.
"""

import heapq
from collections import deque
from typing import List, Tuple, Optional

def dijkstra(n: int, graph: List[List[Tuple[int, int]]], start: int, 
             one_indexed: bool = True) -> List[int]:
    """
    Dijkstra's algorithm for single-source shortest paths
    
    Args:
        n: Number of vertices
        graph: Weighted adjacency list [(neighbor, weight), ...]
        start: Starting vertex
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        List of shortest distances from start
        
    Time: O((V + E) log V), Space: O(V)
    """
    INF = 10**18
    
    if one_indexed:
        dist = [INF] * (n + 1)
    else:
        dist = [INF] * n
    
    dist[start] = 0
    heap = [(0, start)]  # (distance, vertex)
    
    while heap:
        d, u = heapq.heappop(heap)
        
        if d > dist[u]:
            continue
        
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    
    return dist

def dijkstra_with_path(n: int, graph: List[List[Tuple[int, int]]], start: int,
                      one_indexed: bool = True) -> Tuple[List[int], List[int]]:
    """
    Dijkstra with path reconstruction
    
    Args:
        n: Number of vertices
        graph: Weighted adjacency list
        start: Starting vertex
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        (distances, parent) where parent[v] is the previous vertex in shortest path
    """
    INF = 10**18
    
    if one_indexed:
        dist = [INF] * (n + 1)
        parent = [-1] * (n + 1)
    else:
        dist = [INF] * n
        parent = [-1] * n
    
    dist[start] = 0
    heap = [(0, start)]
    
    while heap:
        d, u = heapq.heappop(heap)
        
        if d > dist[u]:
            continue
        
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(heap, (dist[v], v))
    
    return dist, parent

def reconstruct_path(parent: List[int], start: int, end: int) -> List[int]:
    """
    Reconstruct path from parent array
    
    Args:
        parent: Parent array from shortest path algorithm
        start: Starting vertex
        end: Ending vertex
        
    Returns:
        Path from start to end, empty list if no path exists
    """
    if parent[end] == -1 and start != end:
        return []
    
    path = []
    curr = end
    
    while curr != -1:
        path.append(curr)
        curr = parent[curr]
    
    path.reverse()
    return path

def bfs_01(n: int, graph: List[List[Tuple[int, int]]], start: int,
           one_indexed: bool = True) -> List[int]:
    """
    0-1 BFS for graphs with edge weights 0 or 1
    
    Args:
        n: Number of vertices
        graph: Weighted adjacency list (weights must be 0 or 1)
        start: Starting vertex
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        List of shortest distances from start
        
    Time: O(V + E), Space: O(V)
    """
    INF = 10**18
    
    if one_indexed:
        dist = [INF] * (n + 1)
    else:
        dist = [INF] * n
    
    dist[start] = 0
    dq = deque([start])
    
    while dq:
        u = dq.popleft()
        
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                
                if w == 0:
                    dq.appendleft(v)  # 0-weight edges go to front
                else:
                    dq.append(v)      # 1-weight edges go to back
    
    return dist

def floyd_warshall(dist: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Floyd-Warshall algorithm for all-pairs shortest paths
    
    Args:
        dist: Distance matrix where dist[i][j] is weight of edge i->j
              (use INF for no edge, 0 for diagonal)
        
    Returns:
        (distance_matrix, next_matrix) for path reconstruction
        
    Time: O(V^3), Space: O(V^2)
    """
    n = len(dist)
    
    # Initialize next matrix for path reconstruction
    next_matrix = [[-1] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] < 10**18:
                next_matrix[i][j] = j
    
    # Floyd-Warshall main loop
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_matrix[i][j] = next_matrix[i][k]
    
    return dist, next_matrix

def reconstruct_floyd_path(next_matrix: List[List[int]], i: int, j: int) -> List[int]:
    """
    Reconstruct path from Floyd-Warshall next matrix
    
    Args:
        next_matrix: Next matrix from Floyd-Warshall
        i, j: Start and end vertices
        
    Returns:
        Path from i to j, empty list if no path exists
    """
    if next_matrix[i][j] == -1:
        return []
    
    path = [i]
    while i != j:
        i = next_matrix[i][j]
        path.append(i)
    
    return path

def bellman_ford(n: int, edges: List[Tuple[int, int, int]], start: int,
                one_indexed: bool = True) -> Tuple[List[int], bool]:
    """
    Bellman-Ford algorithm for shortest paths with negative weights
    
    Args:
        n: Number of vertices
        edges: List of (u, v, weight) edges
        start: Starting vertex
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        (distances, has_negative_cycle)
        
    Time: O(VE), Space: O(V)
    """
    INF = 10**18
    
    if one_indexed:
        dist = [INF] * (n + 1)
    else:
        dist = [INF] * n
    
    dist[start] = 0
    
    # Relax edges n-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    
    # Check for negative cycles
    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break
    
    return dist, has_negative_cycle