# -*- coding: utf-8 -*-
"""
Linked List implementation with comprehensive operations
"""

from typing import Any, Optional

class LNode:
    """Node for linked list"""
    def __init__(self, data: Any, next_node: Optional['LNode'] = None):
        self.data = data
        self.next = next_node

class LinkedList:
    """
    Singly linked list with common operations
    """
    def __init__(self):
        self.head: Optional[LNode] = None
        self.length = 0

    def __len__(self) -> int:
        """Get length of the list"""
        return self.length

    def __str__(self) -> str:
        """String representation of the list"""
        res = "Head"
        if self.head is None:
            return f"{res} → None"
        
        node = self.head
        while node is not None:
            res = f"{res} → {str(node.data)}"
            node = node.next
        return res

    def __contains__(self, target: Any) -> bool:
        """Check if target exists in the list"""
        if self.head is None:
            return False
        
        node = self.head
        while node is not None:
            if node.data == target:
                return True
            node = node.next
        return False

    def appendleft(self, data: Any) -> None:
        """Add element at the beginning"""
        if self.head is None:
            self.head = LNode(data)
        else:
            self.head = LNode(data, self.head)
        self.length += 1

    def append(self, data: Any) -> None:
        """Add element at the end"""
        if self.head is None:
            self.head = LNode(data)
        else:
            node = self.head
            while node.next is not None:
                node = node.next
            node.next = LNode(data)
        self.length += 1

    def insert(self, index: int, data: Any) -> None:
        """Insert element at given index"""
        if index < 0 or index > self.length:
            raise IndexError("Index out of range")
        
        if index == 0:
            self.appendleft(data)
            return
        
        node = self.head
        for _ in range(index - 1):
            node = node.next
        
        new_node = LNode(data, node.next)
        node.next = new_node
        self.length += 1

    def popleft(self) -> Optional[Any]:
        """Remove and return first element"""
        if self.head is None:
            return None
        
        data = self.head.data
        self.head = self.head.next
        self.length -= 1
        return data

    def pop(self) -> Optional[Any]:
        """Remove and return last element"""
        if self.head is None:
            return None
        
        if self.head.next is None:
            data = self.head.data
            self.head = None
            self.length -= 1
            return data
        
        prev = None
        node = self.head
        while node.next is not None:
            prev = node
            node = node.next
        
        prev.next = None
        self.length -= 1
        return node.data

    def remove(self, target: Any) -> bool:
        """Remove first occurrence of target"""
        if self.head is None:
            return False
        
        if self.head.data == target:
            self.head = self.head.next
            self.length -= 1
            return True
        
        prev = self.head
        node = self.head.next
        while node is not None:
            if node.data == target:
                prev.next = node.next
                self.length -= 1
                return True
            prev = node
            node = node.next
        
        return False

    def reverse(self) -> None:
        """Reverse the linked list in-place"""
        prev = None
        current = self.head
        
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev

    def get(self, index: int) -> Any:
        """Get element at given index"""
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")
        
        node = self.head
        for _ in range(index):
            node = node.next
        
        return node.data

    def clear(self) -> None:
        """Clear all elements"""
        self.head = None
        self.length = 0