# -*- coding: utf-8 -*-
"""
Graph traversal algorithms: BFS and DFS implementations
"""

from collections import deque
from typing import List, Tuple, Dict, Set, Optional

def build_graph(n: int, edges: List[Tuple[int, int]], directed: bool = False, 
                one_indexed: bool = True) -> List[List[int]]:
    """
    Build adjacency list representation of graph
    
    Args:
        n: Number of vertices
        edges: List of (u, v) edges
        directed: Whether graph is directed
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        Adjacency list representation
    """
    if one_indexed:
        graph = [[] for _ in range(n + 1)]
    else:
        graph = [[] for _ in range(n)]
    
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    
    return graph

def build_weighted_graph(n: int, edges: List[Tuple[int, int, int]], 
                        directed: bool = False, one_indexed: bool = True) -> List[List[Tuple[int, int]]]:
    """
    Build weighted adjacency list representation
    
    Args:
        n: Number of vertices
        edges: List of (u, v, weight) edges
        directed: Whether graph is directed
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        Weighted adjacency list where each edge is (neighbor, weight)
    """
    if one_indexed:
        graph = [[] for _ in range(n + 1)]
    else:
        graph = [[] for _ in range(n)]
    
    for u, v, w in edges:
        graph[u].append((v, w))
        if not directed:
            graph[v].append((u, w))
    
    return graph

def bfs_graph(n: int, graph: List[List[int]], start: int, 
              one_indexed: bool = True) -> List[int]:
    """
    BFS traversal returning distances from start vertex
    
    Args:
        n: Number of vertices
        graph: Adjacency list representation
        start: Starting vertex
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        List of distances from start (-1 if unreachable)
        
    Time: O(V + E), Space: O(V)
    """
    if one_indexed:
        dist = [-1] * (n + 1)
    else:
        dist = [-1] * n
    
    dist[start] = 0
    queue = deque([start])
    
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    
    return dist

def bfs_grid(grid: List[str], start_r: int, start_c: int, 
             target: str = '.') -> List[List[int]]:
    """
    BFS on 2D grid
    
    Args:
        grid: 2D grid as list of strings
        start_r, start_c: Starting position
        target: Character representing walkable cells
        
    Returns:
        2D array of distances (-1 if unreachable)
        
    Time: O(R * C), Space: O(R * C)
    """
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    
    if grid[start_r][start_c] != target:
        return dist
    
    dist[start_r][start_c] = 0
    queue = deque([(start_r, start_c)])
    
    # 4-directional movement
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        r, c = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if (0 <= nr < rows and 0 <= nc < cols and 
                grid[nr][nc] == target and dist[nr][nc] == -1):
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    
    return dist

def dfs_graph(graph: List[List[int]], start: int, visited: Optional[Set[int]] = None) -> List[int]:
    """
    DFS traversal returning visited order
    
    Args:
        graph: Adjacency list representation
        start: Starting vertex
        visited: Set of already visited vertices (for multiple components)
        
    Returns:
        List of vertices in DFS order
        
    Time: O(V + E), Space: O(V)
    """
    if visited is None:
        visited = set()
    
    result = []
    stack = [start]
    
    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            result.append(u)
            
            # Add neighbors in reverse order to maintain left-to-right traversal
            for v in reversed(graph[u]):
                if v not in visited:
                    stack.append(v)
    
    return result

def dfs_recursive(graph: List[List[int]], u: int, visited: Set[int], result: List[int]):
    """
    Recursive DFS implementation
    
    Args:
        graph: Adjacency list representation
        u: Current vertex
        visited: Set of visited vertices
        result: List to store DFS order
    """
    visited.add(u)
    result.append(u)
    
    for v in graph[u]:
        if v not in visited:
            dfs_recursive(graph, v, visited, result)

def find_connected_components(n: int, graph: List[List[int]], 
                             one_indexed: bool = True) -> List[List[int]]:
    """
    Find all connected components in undirected graph
    
    Args:
        n: Number of vertices
        graph: Adjacency list representation
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        List of components, each component is a list of vertices
        
    Time: O(V + E), Space: O(V)
    """
    visited = set()
    components = []
    
    start = 1 if one_indexed else 0
    end = n + 1 if one_indexed else n
    
    for u in range(start, end):
        if u not in visited:
            component = dfs_graph(graph, u, visited)
            components.append(component)
    
    return components

def has_cycle_undirected(n: int, graph: List[List[int]], 
                        one_indexed: bool = True) -> bool:
    """
    Check if undirected graph has a cycle
    
    Args:
        n: Number of vertices
        graph: Adjacency list representation
        one_indexed: Whether vertices are 1-indexed
        
    Returns:
        True if graph has a cycle
        
    Time: O(V + E), Space: O(V)
    """
    visited = set()
    
    def dfs(u: int, parent: int) -> bool:
        visited.add(u)
        
        for v in graph[u]:
            if v == parent:
                continue
            if v in visited or dfs(v, u):
                return True
        
        return False
    
    start = 1 if one_indexed else 0
    end = n + 1 if one_indexed else n
    
    for u in range(start, end):
        if u not in visited:
            if dfs(u, -1):
                return True
    
    return False