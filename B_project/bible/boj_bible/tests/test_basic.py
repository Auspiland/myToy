# -*- coding: utf-8 -*-
"""
Basic tests for BOJ Bible library
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boj_bible.basic.stack_queue import Stack, Queue, next_greater_indices, sliding_window_min
from boj_bible.basic.union_find import DSU
from boj_bible.basic.linked_list import LinkedList


class TestStack(unittest.TestCase):
    def test_stack_operations(self):
        stack = Stack()
        self.assertTrue(stack.empty())
        
        stack.push(1)
        stack.push(2)
        stack.push(3)
        
        self.assertFalse(stack.empty())
        self.assertEqual(stack.size(), 3)
        self.assertEqual(stack.top(), 3)
        
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.size(), 1)


class TestQueue(unittest.TestCase):
    def test_queue_operations(self):
        queue = Queue()
        self.assertTrue(queue.empty())
        
        queue.push(1)
        queue.push(2)
        queue.push(3)
        
        self.assertFalse(queue.empty())
        self.assertEqual(queue.size(), 3)
        
        self.assertEqual(queue.pop(), 1)
        self.assertEqual(queue.pop(), 2)
        self.assertEqual(queue.size(), 1)


class TestMonotonicStackQueue(unittest.TestCase):
    def test_next_greater_indices(self):
        arr = [3, 5, 2, 7]
        result = next_greater_indices(arr)
        expected = [1, 3, 3, -1]
        self.assertEqual(result, expected)
        
        arr = [1, 2, 3, 4]
        result = next_greater_indices(arr)
        expected = [1, 2, 3, -1]
        self.assertEqual(result, expected)
    
    def test_sliding_window_min(self):
        arr = [1, 3, -1, -3, 5, 3, 6, 7]
        k = 3
        result = sliding_window_min(arr, k)
        expected = [-1, -3, -3, -3, 3, 3]
        self.assertEqual(result, expected)


class TestDSU(unittest.TestCase):
    def test_union_find(self):
        dsu = DSU(5)
        
        # Initial state
        self.assertEqual(dsu.num_components(), 5)
        self.assertFalse(dsu.connected(0, 1))
        self.assertEqual(dsu.component_size(0), 1)
        
        # Union operations
        self.assertTrue(dsu.union(0, 1))
        self.assertTrue(dsu.connected(0, 1))
        self.assertEqual(dsu.component_size(0), 2)
        self.assertEqual(dsu.num_components(), 4)
        
        # Union same components
        self.assertFalse(dsu.union(0, 1))
        self.assertEqual(dsu.num_components(), 4)
        
        # More unions
        dsu.union(2, 3)
        dsu.union(0, 2)
        self.assertTrue(dsu.connected(1, 3))
        self.assertEqual(dsu.component_size(0), 4)


class TestLinkedList(unittest.TestCase):
    def test_linked_list_operations(self):
        ll = LinkedList()
        self.assertEqual(len(ll), 0)
        
        # Append operations
        ll.append(1)
        ll.append(2)
        ll.appendleft(0)
        
        self.assertEqual(len(ll), 3)
        self.assertIn(1, ll)
        self.assertNotIn(5, ll)
        
        # Pop operations
        self.assertEqual(ll.popleft(), 0)
        self.assertEqual(ll.pop(), 2)
        self.assertEqual(len(ll), 1)
        
        # Insert and remove
        ll.insert(0, 5)
        ll.insert(2, 10)
        self.assertTrue(ll.remove(5))
        self.assertFalse(ll.remove(99))


if __name__ == '__main__':
    unittest.main()