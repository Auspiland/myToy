# -*- coding: utf-8 -*-
"""
Tree algorithm tests
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boj_bible.tree.segment_tree import SegTreeSum, SegTreeMin, FenwickTree
from boj_bible.tree.lca import LCA


class TestSegmentTree(unittest.TestCase):
    def test_segment_tree_sum(self):
        arr = [1, 2, 3, 4, 5]
        st = SegTreeSum(arr)
        
        # Test range sum
        self.assertEqual(st.query(0, 2), 6)  # 1+2+3
        self.assertEqual(st.query(1, 4), 14)  # 2+3+4+5
        
        # Test update
        st.update(2, 10)  # Change 3 to 10
        self.assertEqual(st.query(0, 2), 13)  # 1+2+10
        self.assertEqual(st.query(2, 2), 10)  # Just 10
    
    def test_segment_tree_min(self):
        arr = [5, 2, 8, 1, 3]
        st = SegTreeMin(arr)
        
        # Test range minimum
        self.assertEqual(st.query(0, 2), 2)
        self.assertEqual(st.query(1, 4), 1)
        
        # Test update
        st.update(3, 0)  # Change 1 to 0
        self.assertEqual(st.query(1, 4), 0)


class TestFenwickTree(unittest.TestCase):
    def test_fenwick_tree(self):
        bit = FenwickTree(5)
        
        # Add values: [0, 1, 2, 3, 4, 5] (1-indexed)
        for i in range(1, 6):
            bit.add(i, i)
        
        # Test prefix sums
        self.assertEqual(bit.sum(3), 6)  # 1+2+3
        self.assertEqual(bit.sum(5), 15)  # 1+2+3+4+5
        
        # Test range sum
        self.assertEqual(bit.range_sum(2, 4), 9)  # 2+3+4
        
        # Test update
        bit.update(3, 10)  # Change position 3 to 10
        self.assertEqual(bit.range_sum(2, 4), 16)  # 2+10+4


class TestLCA(unittest.TestCase):
    def test_lca(self):
        # Tree: 1-2, 1-3, 2-4, 2-5, 3-6
        tree = [
            [],          # 0 (unused)
            [2, 3],      # 1
            [1, 4, 5],   # 2  
            [1, 6],      # 3
            [2],         # 4
            [2],         # 5
            [3]          # 6
        ]
        
        lca = LCA(6, tree, root=1)
        
        # Test LCA queries
        self.assertEqual(lca.lca(4, 5), 2)  # Both children of 2
        self.assertEqual(lca.lca(4, 6), 1)  # LCA is root
        self.assertEqual(lca.lca(2, 3), 1)  # LCA is root
        self.assertEqual(lca.lca(4, 4), 4)  # Same node
        
        # Test distances
        self.assertEqual(lca.dist(4, 5), 2)  # 4->2->5
        self.assertEqual(lca.dist(4, 6), 4)  # 4->2->1->3->6
        self.assertEqual(lca.dist(1, 4), 2)  # 1->2->4


if __name__ == '__main__':
    unittest.main()