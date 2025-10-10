# -*- coding: utf-8 -*-
"""
Graph algorithm tests
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boj_bible.graph.bfs_dfs import build_graph, bfs_graph, find_connected_components
from boj_bible.graph.shortest_path import dijkstra, floyd_warshall
from boj_bible.graph.topological_sort import topological_sort_kahn


class TestGraphBuilding(unittest.TestCase):
    def test_build_graph(self):
        edges = [(1, 2), (2, 3), (1, 3)]
        graph = build_graph(3, edges, directed=False, one_indexed=True)
        
        self.assertEqual(len(graph), 4)  # 0 unused, 1-3 used
        self.assertIn(2, graph[1])
        self.assertIn(3, graph[1])
        self.assertIn(1, graph[2])
        self.assertIn(3, graph[2])


class TestBFS(unittest.TestCase):
    def test_bfs_graph(self):
        edges = [(1, 2), (2, 3), (3, 4)]
        graph = build_graph(4, edges, directed=False, one_indexed=True)
        
        distances = bfs_graph(4, graph, 1, one_indexed=True)
        
        expected = [-1, 0, 1, 2, 3]  # distances[0] unused
        self.assertEqual(distances, expected)


class TestConnectedComponents(unittest.TestCase):
    def test_connected_components(self):
        edges = [(1, 2), (3, 4)]  # Two separate components
        graph = build_graph(4, edges, directed=False, one_indexed=True)
        
        components = find_connected_components(4, graph, one_indexed=True)
        
        self.assertEqual(len(components), 2)
        # Sort components for consistent testing
        components = [sorted(comp) for comp in components]
        components.sort()
        
        expected = [[1, 2], [3, 4]]
        self.assertEqual(components, expected)


class TestDijkstra(unittest.TestCase):
    def test_dijkstra(self):
        # Weighted graph: 1-2 (weight 1), 2-3 (weight 2), 1-3 (weight 4)
        graph = [[], [(2, 1), (3, 4)], [(1, 1), (3, 2)], [(1, 4), (2, 2)]]
        
        distances = dijkstra(3, graph, 1, one_indexed=True)
        
        expected = [float('inf'), 0, 1, 3]  # 1->1: 0, 1->2: 1, 1->3: 3
        # Allow for INF representation differences
        self.assertEqual(distances[1], 0)
        self.assertEqual(distances[2], 1)
        self.assertEqual(distances[3], 3)


class TestFloydWarshall(unittest.TestCase):
    def test_floyd_warshall(self):
        INF = 10**18
        # 3x3 adjacency matrix
        dist = [
            [0, 1, INF],
            [INF, 0, 2],
            [4, INF, 0]
        ]
        
        result_dist, next_matrix = floyd_warshall(dist)
        
        # Check shortest path 0->2 should be 0->1->2 = 3
        self.assertEqual(result_dist[0][2], 3)
        self.assertEqual(result_dist[2][0], 4)


class TestTopologicalSort(unittest.TestCase):
    def test_topological_sort_kahn(self):
        # DAG: 1->2, 1->3, 2->3
        graph = [[], [2, 3], [3], []]
        
        topo_order = topological_sort_kahn(3, graph, one_indexed=True)
        
        self.assertIsNotNone(topo_order)
        self.assertEqual(len(topo_order), 3)
        
        # Check that 1 comes before 2 and 3, and 2 comes before 3
        pos = {node: i for i, node in enumerate(topo_order)}
        self.assertLess(pos[1], pos[2])
        self.assertLess(pos[1], pos[3])
        self.assertLess(pos[2], pos[3])


if __name__ == '__main__':
    unittest.main()