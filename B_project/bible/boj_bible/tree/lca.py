# -*- coding: utf-8 -*-
"""
Lowest Common Ancestor (LCA) algorithms and tree utilities
"""

import math
from typing import List, Tuple, Optional

class LCA:
    """
    LCA using binary lifting (sparse table approach)
    """
    def __init__(self, n: int, tree: List[List[int]], root: int = 1):
        """
        Initialize LCA data structure
        
        Args:
            n: Number of vertices
            tree: Adjacency list representation of tree
            root: Root of the tree
        """
        self.n = n
        self.LOG = int(math.log2(n)) + 1
        self.tree = tree
        self.root = root
        
        # Initialize arrays
        self.depth = [0] * (n + 1)
        self.parent = [[-1] * self.LOG for _ in range(n + 1)]
        
        # Build LCA table
        self._dfs(root, -1, 0)
        self._preprocess()
    
    def _dfs(self, u: int, p: int, d: int):
        """DFS to compute depth and immediate parent"""
        self.depth[u] = d
        self.parent[u][0] = p
        
        for v in self.tree[u]:
            if v != p:
                self._dfs(v, u, d + 1)
    
    def _preprocess(self):
        """Preprocess sparse table for LCA"""
        for j in range(1, self.LOG):
            for i in range(1, self.n + 1):
                if self.parent[i][j - 1] != -1:
                    self.parent[i][j] = self.parent[self.parent[i][j - 1]][j - 1]
    
    def lca(self, u: int, v: int) -> int:
        """
        Find LCA of vertices u and v
        
        Args:
            u, v: Vertices to find LCA for
            
        Returns:
            LCA of u and v
            
        Time: O(log n)
        """
        # Make u the deeper vertex
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        
        # Bring u to the same level as v
        diff = self.depth[u] - self.depth[v]
        for i in range(self.LOG):
            if (diff >> i) & 1:
                u = self.parent[u][i]
        
        # If u and v are the same, return u
        if u == v:
            return u
        
        # Binary search for LCA
        for i in range(self.LOG - 1, -1, -1):
            if self.parent[u][i] != self.parent[v][i]:
                u = self.parent[u][i]
                v = self.parent[v][i]
        
        return self.parent[u][0]
    
    def dist(self, u: int, v: int) -> int:
        """
        Find distance between vertices u and v
        
        Args:
            u, v: Vertices to find distance for
            
        Returns:
            Distance between u and v
            
        Time: O(log n)
        """
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]
    
    def is_ancestor(self, u: int, v: int) -> bool:
        """
        Check if u is ancestor of v
        
        Args:
            u, v: Vertices to check
            
        Returns:
            True if u is ancestor of v
            
        Time: O(log n)
        """
        return self.lca(u, v) == u

class WeightedLCA:
    """
    LCA for weighted trees with distance queries
    """
    def __init__(self, n: int, tree: List[List[Tuple[int, int]]], root: int = 1):
        """
        Initialize weighted LCA
        
        Args:
            n: Number of vertices
            tree: Weighted adjacency list [(neighbor, weight), ...]
            root: Root of the tree
        """
        self.n = n
        self.LOG = int(math.log2(n)) + 1
        self.tree = tree
        self.root = root
        
        # Initialize arrays
        self.depth = [0] * (n + 1)
        self.dist_from_root = [0] * (n + 1)
        self.parent = [[-1] * self.LOG for _ in range(n + 1)]
        
        # Build LCA table
        self._dfs(root, -1, 0, 0)
        self._preprocess()
    
    def _dfs(self, u: int, p: int, d: int, dist: int):
        """DFS to compute depth, distance, and parent"""
        self.depth[u] = d
        self.dist_from_root[u] = dist
        self.parent[u][0] = p
        
        for v, w in self.tree[u]:
            if v != p:
                self._dfs(v, u, d + 1, dist + w)
    
    def _preprocess(self):
        """Preprocess sparse table for LCA"""
        for j in range(1, self.LOG):
            for i in range(1, self.n + 1):
                if self.parent[i][j - 1] != -1:
                    self.parent[i][j] = self.parent[self.parent[i][j - 1]][j - 1]
    
    def lca(self, u: int, v: int) -> int:
        """Find LCA of vertices u and v"""
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        
        diff = self.depth[u] - self.depth[v]
        for i in range(self.LOG):
            if (diff >> i) & 1:
                u = self.parent[u][i]
        
        if u == v:
            return u
        
        for i in range(self.LOG - 1, -1, -1):
            if self.parent[u][i] != self.parent[v][i]:
                u = self.parent[u][i]
                v = self.parent[v][i]
        
        return self.parent[u][0]
    
    def dist(self, u: int, v: int) -> int:
        """
        Find weighted distance between vertices u and v
        
        Args:
            u, v: Vertices to find distance for
            
        Returns:
            Weighted distance between u and v
            
        Time: O(log n)
        """
        lca_node = self.lca(u, v)
        return (self.dist_from_root[u] + self.dist_from_root[v] - 
                2 * self.dist_from_root[lca_node])

def tree_diameter(n: int, tree: List[List[Tuple[int, int]]]) -> Tuple[int, int, int]:
    """
    Find diameter of weighted tree using two DFS calls
    
    Args:
        n: Number of vertices
        tree: Weighted adjacency list [(neighbor, weight), ...]
        
    Returns:
        (endpoint1, endpoint2, diameter) where diameter is the maximum distance
        
    Time: O(n), Space: O(n)
    """
    def dfs(start: int) -> Tuple[int, int]:
        """
        DFS to find farthest vertex and its distance from start
        """
        visited = [False] * (n + 1)
        max_dist = 0
        farthest = start
        
        def dfs_helper(u: int, dist: int):
            nonlocal max_dist, farthest
            visited[u] = True
            
            if dist > max_dist:
                max_dist = dist
                farthest = u
            
            for v, w in tree[u]:
                if not visited[v]:
                    dfs_helper(v, dist + w)
        
        dfs_helper(start, 0)
        return farthest, max_dist
    
    # First DFS to find one end of diameter
    u, _ = dfs(1)
    
    # Second DFS to find other end and diameter
    v, diameter = dfs(u)
    
    return u, v, diameter

def tree_centroid(n: int, tree: List[List[int]]) -> List[int]:
    """
    Find centroid(s) of tree
    
    Args:
        n: Number of vertices
        tree: Adjacency list representation
        
    Returns:
        List of centroids (1 or 2 vertices)
        
    Time: O(n), Space: O(n)
    """
    subtree_size = [0] * (n + 1)
    
    def dfs_size(u: int, parent: int) -> int:
        """Calculate subtree sizes"""
        subtree_size[u] = 1
        for v in tree[u]:
            if v != parent:
                subtree_size[u] += dfs_size(v, u)
        return subtree_size[u]
    
    dfs_size(1, -1)
    
    def find_centroid(u: int, parent: int) -> Optional[int]:
        """Find centroid starting from u"""
        for v in tree[u]:
            if v != parent and subtree_size[v] > n // 2:
                return find_centroid(v, u)
        return u
    
    centroid = find_centroid(1, -1)
    centroids = [centroid]
    
    # Check if there's a second centroid
    for v in tree[centroid]:
        if subtree_size[v] == n // 2:
            centroids.append(v)
            break
    
    return sorted(centroids)