# -*- coding: utf-8 -*-
"""
Topological sorting algorithms for directed acyclic graphs (DAGs)
"""

from collections import deque
from typing import List, Optional, Tuple

def topological_sort_kahn(n: int, graph: List[List[int]], 
                         one_indexed: bool = True) -> Optional[List[int]]:
    """
    Topological sort using Kahn's algorithm (BFS-based)
    
    Args:
        n: Number of vertices
        graph: Adjacency list representation of directed graph
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        Topologically sorted order, None if graph has cycle
        
    Time: O(V + E), Space: O(V)
    """
    # Calculate in-degrees
    if one_indexed:
        indegree = [0] * (n + 1)
        start, end = 1, n + 1
    else:
        indegree = [0] * n
        start, end = 0, n
    
    for u in range(start, end):
        for v in graph[u]:
            indegree[v] += 1
    
    # Initialize queue with vertices having in-degree 0
    queue = deque()
    for u in range(start, end):
        if indegree[u] == 0:
            queue.append(u)
    
    result = []
    
    while queue:
        u = queue.popleft()
        result.append(u)
        
        # Remove u and decrease in-degrees of neighbors
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    
    # Check if all vertices are included (no cycle)
    if len(result) == n:
        return result
    else:
        return None  # Graph has cycle

def topological_sort_dfs(n: int, graph: List[List[int]], 
                        one_indexed: bool = True) -> Optional[List[int]]:
    """
    Topological sort using DFS
    
    Args:
        n: Number of vertices
        graph: Adjacency list representation of directed graph
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        Topologically sorted order, None if graph has cycle
        
    Time: O(V + E), Space: O(V)
    """
    if one_indexed:
        start, end = 1, n + 1
    else:
        start, end = 0, n
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * (end)
    result = []
    
    def dfs(u: int) -> bool:
        """
        Returns True if cycle detected
        """
        color[u] = GRAY
        
        for v in graph[u]:
            if color[v] == GRAY:  # Back edge - cycle detected
                return True
            if color[v] == WHITE and dfs(v):
                return True
        
        color[u] = BLACK
        result.append(u)
        return False
    
    # Run DFS from all unvisited vertices
    for u in range(start, end):
        if color[u] == WHITE:
            if dfs(u):
                return None  # Cycle detected
    
    result.reverse()  # Reverse to get correct topological order
    return result

def has_cycle_directed(n: int, graph: List[List[int]], 
                      one_indexed: bool = True) -> bool:
    """
    Check if directed graph has a cycle using DFS
    
    Args:
        n: Number of vertices
        graph: Adjacency list representation of directed graph
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        True if graph has a cycle
        
    Time: O(V + E), Space: O(V)
    """
    if one_indexed:
        start, end = 1, n + 1
    else:
        start, end = 0, n
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * end
    
    def dfs(u: int) -> bool:
        color[u] = GRAY
        
        for v in graph[u]:
            if color[v] == GRAY or (color[v] == WHITE and dfs(v)):
                return True
        
        color[u] = BLACK
        return False
    
    for u in range(start, end):
        if color[u] == WHITE and dfs(u):
            return True
    
    return False

def longest_path_dag(n: int, graph: List[List[Tuple[int, int]]], start: int,
                    one_indexed: bool = True) -> List[int]:
    """
    Find longest path in DAG using topological sort
    
    Args:
        n: Number of vertices
        graph: Weighted adjacency list [(neighbor, weight), ...]
        start: Starting vertex
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        List of longest distances from start (-INF if unreachable)
        
    Time: O(V + E), Space: O(V)
    """
    # Convert weighted graph to unweighted for topological sort
    unweighted_graph = []
    if one_indexed:
        unweighted_graph = [[] for _ in range(n + 1)]
        dist = [-float('inf')] * (n + 1)
    else:
        unweighted_graph = [[] for _ in range(n)]
        dist = [-float('inf')] * n
    
    for u in range(len(graph)):
        for v, w in graph[u]:
            unweighted_graph[u].append(v)
    
    # Get topological order
    topo_order = topological_sort_kahn(n, unweighted_graph, one_indexed)
    if topo_order is None:
        return dist  # Graph has cycle
    
    dist[start] = 0
    
    # Process vertices in topological order
    for u in topo_order:
        if dist[u] != -float('inf'):
            for v, w in graph[u]:
                dist[v] = max(dist[v], dist[u] + w)
    
    return dist

def count_paths_dag(n: int, graph: List[List[int]], start: int, end: int,
                   one_indexed: bool = True, mod: int = 10**9 + 7) -> int:
    """
    Count number of paths from start to end in DAG
    
    Args:
        n: Number of vertices
        graph: Adjacency list representation
        start: Starting vertex
        end: Ending vertex
        one_indexed: Whether vertices are 1-indexed
        mod: Modulo for counting
        
    Returns:
        Number of paths from start to end
        
    Time: O(V + E), Space: O(V)
    """
    # Get topological order
    topo_order = topological_sort_kahn(n, graph, one_indexed)
    if topo_order is None:
        return 0  # Graph has cycle
    
    if one_indexed:
        dp = [0] * (n + 1)
    else:
        dp = [0] * n
    
    dp[start] = 1
    
    # Process vertices in topological order
    for u in topo_order:
        if dp[u] > 0:
            for v in graph[u]:
                dp[v] = (dp[v] + dp[u]) % mod
    
    return dp[end]