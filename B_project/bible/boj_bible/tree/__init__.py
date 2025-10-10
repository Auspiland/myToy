# -*- coding: utf-8 -*-
"""
Tree algorithms module
"""

from .segment_tree import (
    SegmentTree, SegTreeSum, SegTreeMin, SegTreeMax,
    LazySegmentTree, FenwickTree
)
from .lca import (
    LCA, WeightedLCA, tree_diameter, tree_centroid
)

__all__ = [
    # Segment trees
    'SegmentTree', 'SegTreeSum', 'SegTreeMin', 'SegTreeMax',
    'LazySegmentTree', 'FenwickTree',
    
    # LCA and tree utilities
    'LCA', 'WeightedLCA', 'tree_diameter', 'tree_centroid'
]