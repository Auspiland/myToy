# -*- coding: utf-8 -*-
"""
Basic data structures: Stack, Queue, Deque, and Monotonic Stack/Queue
"""

from collections import deque
from typing import List, Optional, Any

class Stack:
    """Simple stack implementation using list"""
    def __init__(self):
        self._s = []
    
    def push(self, x: Any) -> None:
        """Push element to top of stack"""
        self._s.append(x)
    
    def pop(self) -> Any:
        """Pop element from top of stack"""
        return self._s.pop()
    
    def top(self) -> Any:
        """Get top element without removing"""
        return self._s[-1]
    
    def empty(self) -> bool:
        """Check if stack is empty"""
        return not self._s
    
    def size(self) -> int:
        """Get stack size"""
        return len(self._s)

class Queue:
    """Simple queue implementation using deque"""
    def __init__(self):
        self._q = deque()
    
    def push(self, x: Any) -> None:
        """Push element to back of queue"""
        self._q.append(x)
    
    def pop(self) -> Any:
        """Pop element from front of queue"""
        return self._q.popleft()
    
    def empty(self) -> bool:
        """Check if queue is empty"""
        return not self._q
    
    def size(self) -> int:
        """Get queue size"""
        return len(self._q)

def next_greater_indices(arr: List[int]) -> List[int]:
    """
    Find next greater element indices for each element.
    
    Args:
        arr: Input array
        
    Returns:
        List where result[i] is the index of next greater element than arr[i],
        or -1 if no such element exists
        
    Time: O(n), Space: O(n)
    """
    n = len(arr)
    ans = [-1] * n
    st = []  # Monotonic decreasing stack
    
    for i in range(n):
        while st and arr[st[-1]] < arr[i]:
            ans[st.pop()] = i
        st.append(i)
    
    return ans

def sliding_window_min(arr: List[int], k: int) -> List[int]:
    """
    Find minimum in each sliding window of size k.
    
    Args:
        arr: Input array
        k: Window size
        
    Returns:
        List of minimums for each window
        
    Time: O(n), Space: O(k)
    """
    if not arr or k <= 0:
        return []
    
    n = len(arr)
    dq = deque()  # Stores indices in increasing order of values
    res = []
    
    for i in range(n):
        # Remove indices outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Maintain monotonic property
        while dq and arr[dq[-1]] >= arr[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            res.append(arr[dq[0]])
    
    return res

def sliding_window_max(arr: List[int], k: int) -> List[int]:
    """
    Find maximum in each sliding window of size k.
    
    Args:
        arr: Input array
        k: Window size
        
    Returns:
        List of maximums for each window
        
    Time: O(n), Space: O(k)
    """
    if not arr or k <= 0:
        return []
    
    n = len(arr)
    dq = deque()  # Stores indices in decreasing order of values
    res = []
    
    for i in range(n):
        # Remove indices outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Maintain monotonic property
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            res.append(arr[dq[0]])
    
    return res