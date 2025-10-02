# -*- coding: utf-8 -*-
"""
BOJ Bible - Competitive Programming Library for Python

A comprehensive collection of data structures and algorithms 
optimized for competitive programming and online judges.
"""

__version__ = "1.0.0"
__author__ = "BOJ Bible Contributors"

# Import main modules
from . import basic
from . import graph  
from . import tree
from . import string
from . import advanced
from . import utils

# Import commonly used classes and functions
from .basic.stack_queue import Stack, Queue, next_greater_indices, sliding_window_min
from .basic.union_find import DSU
from .graph.bfs_dfs import build_graph, bfs_graph, dfs_graph
from .graph.shortest_path import dijkstra, floyd_warshall
from .tree.segment_tree import SegTreeSum, SegTreeMin, FenwickTree
from .tree.lca import LCA
from .string.pattern_matching import kmp_search, z_algorithm
from .string.trie import Trie
from .utils.fast_io import read_int, read_ints, INF

__all__ = [
    # Modules
    'basic', 'graph', 'tree', 'string', 'advanced', 'utils',
    
    # Basic data structures
    'Stack', 'Queue', 'DSU',
    
    # Graph algorithms
    'build_graph', 'bfs_graph', 'dfs_graph', 'dijkstra', 'floyd_warshall',
    
    # Tree algorithms  
    'SegTreeSum', 'SegTreeMin', 'FenwickTree', 'LCA',
    
    # String algorithms
    'kmp_search', 'z_algorithm', 'Trie',
    
    # Utilities
    'read_int', 'read_ints', 'INF',
    'next_greater_indices', 'sliding_window_min'
]