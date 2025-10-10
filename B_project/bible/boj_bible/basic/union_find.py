# -*- coding: utf-8 -*-
"""
Disjoint Set Union (Union-Find) data structure
"""

from typing import List

class DSU:
    """
    Disjoint Set Union with path compression and union by rank
    """
    def __init__(self, n: int):
        """
        Initialize DSU for n elements (0-indexed)
        
        Args:
            n: Number of elements
        """
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        """
        Find root of element x with path compression
        
        Args:
            x: Element to find root for
            
        Returns:
            Root of the component containing x
            
        Time: O(α(n)) amortized
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Union components containing x and y
        
        Args:
            x, y: Elements to union
            
        Returns:
            True if components were different (union performed), False otherwise
            
        Time: O(α(n)) amortized
        """
        px, py = self.find(x), self.find(y)
        
        if px == py:
            return False

        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        
        self.parent[py] = px
        self.size[px] += self.size[py]
        
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """
        Check if x and y are in the same component
        
        Args:
            x, y: Elements to check
            
        Returns:
            True if x and y are connected
            
        Time: O(α(n)) amortized
        """
        return self.find(x) == self.find(y)

    def component_size(self, x: int) -> int:
        """
        Get size of component containing x
        
        Args:
            x: Element to get component size for
            
        Returns:
            Size of component containing x
            
        Time: O(α(n)) amortized
        """
        return self.size[self.find(x)]

    def num_components(self) -> int:
        """
        Get number of components
        
        Returns:
            Number of connected components
            
        Time: O(1)
        """
        return self.components

    def get_components(self) -> List[List[int]]:
        """
        Get all components as lists
        
        Returns:
            List of components, each component is a list of elements
            
        Time: O(n)
        """
        from collections import defaultdict
        
        groups = defaultdict(list)
        for i in range(len(self.parent)):
            groups[self.find(i)].append(i)
        
        return list(groups.values())