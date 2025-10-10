# -*- coding: utf-8 -*-
"""
Segment Tree implementations for range queries and updates
"""

from typing import List, Callable, Any

class SegmentTree:
    """
    Generic segment tree implementation
    """
    def __init__(self, arr: List[Any], combine_fn: Callable[[Any, Any], Any], 
                 identity: Any):
        """
        Initialize segment tree
        
        Args:
            arr: Input array
            combine_fn: Function to combine two values (e.g., min, max, sum)
            identity: Identity element for the operation
        """
        self.n = len(arr)
        self.combine = combine_fn
        self.identity = identity
        self.tree = [identity] * (4 * self.n)
        
        if arr:
            self._build(arr, 1, 0, self.n - 1)
    
    def _build(self, arr: List[Any], node: int, start: int, end: int):
        """Build the segment tree"""
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self._build(arr, 2 * node, start, mid)
            self._build(arr, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.combine(self.tree[2 * node], self.tree[2 * node + 1])
    
    def update(self, idx: int, val: Any):
        """Update element at index idx to val"""
        self._update(1, 0, self.n - 1, idx, val)
    
    def _update(self, node: int, start: int, end: int, idx: int, val: Any):
        """Internal update method"""
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self._update(2 * node, start, mid, idx, val)
            else:
                self._update(2 * node + 1, mid + 1, end, idx, val)
            self.tree[node] = self.combine(self.tree[2 * node], self.tree[2 * node + 1])
    
    def query(self, l: int, r: int) -> Any:
        """Query range [l, r] inclusive"""
        return self._query(1, 0, self.n - 1, l, r)
    
    def _query(self, node: int, start: int, end: int, l: int, r: int) -> Any:
        """Internal query method"""
        if r < start or end < l:
            return self.identity
        if l <= start and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_result = self._query(2 * node, start, mid, l, r)
        right_result = self._query(2 * node + 1, mid + 1, end, l, r)
        return self.combine(left_result, right_result)

class SegTreeSum:
    """Segment tree for range sum queries"""
    def __init__(self, arr: List[int]):
        self.seg_tree = SegmentTree(arr, lambda x, y: x + y, 0)
    
    def update(self, idx: int, val: int):
        """Update element at index idx to val"""
        self.seg_tree.update(idx, val)
    
    def query(self, l: int, r: int) -> int:
        """Query sum of range [l, r]"""
        return self.seg_tree.query(l, r)

class SegTreeMin:
    """Segment tree for range minimum queries"""
    def __init__(self, arr: List[int]):
        self.seg_tree = SegmentTree(arr, min, float('inf'))
    
    def update(self, idx: int, val: int):
        """Update element at index idx to val"""
        self.seg_tree.update(idx, val)
    
    def query(self, l: int, r: int) -> int:
        """Query minimum of range [l, r]"""
        return self.seg_tree.query(l, r)

class SegTreeMax:
    """Segment tree for range maximum queries"""
    def __init__(self, arr: List[int]):
        self.seg_tree = SegmentTree(arr, max, float('-inf'))
    
    def update(self, idx: int, val: int):
        """Update element at index idx to val"""
        self.seg_tree.update(idx, val)
    
    def query(self, l: int, r: int) -> int:
        """Query maximum of range [l, r]"""
        return self.seg_tree.query(l, r)

class LazySegmentTree:
    """
    Segment tree with lazy propagation for range updates
    """
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        
        if arr:
            self._build(arr, 1, 0, self.n - 1)
    
    def _build(self, arr: List[int], node: int, start: int, end: int):
        """Build the segment tree"""
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self._build(arr, 2 * node, start, mid)
            self._build(arr, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def _push(self, node: int, start: int, end: int):
        """Push lazy value down"""
        if self.lazy[node] != 0:
            self.tree[node] += self.lazy[node] * (end - start + 1)
            
            if start != end:  # Not a leaf
                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]
            
            self.lazy[node] = 0
    
    def range_add(self, l: int, r: int, val: int):
        """Add val to all elements in range [l, r]"""
        self._range_add(1, 0, self.n - 1, l, r, val)
    
    def _range_add(self, node: int, start: int, end: int, l: int, r: int, val: int):
        """Internal range add method"""
        self._push(node, start, end)
        
        if start > r or end < l:
            return
        
        if start >= l and end <= r:
            self.lazy[node] += val
            self._push(node, start, end)
            return
        
        mid = (start + end) // 2
        self._range_add(2 * node, start, mid, l, r, val)
        self._range_add(2 * node + 1, mid + 1, end, l, r, val)
        
        self._push(2 * node, start, mid)
        self._push(2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
    
    def range_sum(self, l: int, r: int) -> int:
        """Query sum of range [l, r]"""
        return self._range_sum(1, 0, self.n - 1, l, r)
    
    def _range_sum(self, node: int, start: int, end: int, l: int, r: int) -> int:
        """Internal range sum method"""
        if start > r or end < l:
            return 0
        
        self._push(node, start, end)
        
        if start >= l and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_sum = self._range_sum(2 * node, start, mid, l, r)
        right_sum = self._range_sum(2 * node + 1, mid + 1, end, l, r)
        return left_sum + right_sum

class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree) for prefix sum queries
    1-indexed implementation
    """
    def __init__(self, n: int):
        """
        Initialize Fenwick tree
        
        Args:
            n: Size of the array (1-indexed)
        """
        self.n = n
        self.tree = [0] * (n + 1)
    
    def add(self, idx: int, delta: int):
        """
        Add delta to element at index idx
        
        Args:
            idx: Index to update (1-indexed)
            delta: Value to add
            
        Time: O(log n)
        """
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & (-idx)
    
    def sum(self, idx: int) -> int:
        """
        Get prefix sum up to index idx
        
        Args:
            idx: Index to query (1-indexed)
            
        Returns:
            Sum of elements from 1 to idx
            
        Time: O(log n)
        """
        result = 0
        while idx > 0:
            result += self.tree[idx]
            idx -= idx & (-idx)
        return result
    
    def range_sum(self, l: int, r: int) -> int:
        """
        Get sum of range [l, r]
        
        Args:
            l, r: Range boundaries (1-indexed)
            
        Returns:
            Sum of elements from l to r
            
        Time: O(log n)
        """
        return self.sum(r) - self.sum(l - 1)
    
    def update(self, idx: int, val: int):
        """
        Update element at index idx to val
        
        Args:
            idx: Index to update (1-indexed)
            val: New value
            
        Time: O(log n)
        """
        current = self.range_sum(idx, idx)
        self.add(idx, val - current)