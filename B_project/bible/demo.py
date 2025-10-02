#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOJ Bible 라이브러리 데모
"""

import sys
import os

# Add boj_bible to path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Import from modularized library
from boj_bible.basic import Stack, DSU, next_greater_indices
from boj_bible.graph import build_graph, bfs_graph, dijkstra
from boj_bible.tree import SegTreeSum, FenwickTree
from boj_bible.string import kmp_search, Trie

def demo_basic_structures():
    print("=== 기초 자료구조 데모 ===")
    
    # Stack 데모
    print("\n1. Stack:")
    stack = Stack()
    for i in [1, 2, 3]:
        stack.push(i)
    print(f"Pop: {stack.pop()}, {stack.pop()}")
    
    # DSU 데모
    print("\n2. Union-Find:")
    dsu = DSU(5)
    dsu.union(0, 1)
    dsu.union(2, 3)
    print(f"Connected(0,1): {dsu.connected(0, 1)}")
    print(f"Connected(0,2): {dsu.connected(0, 2)}")
    print(f"Components: {dsu.num_components()}")
    
    # 단조 스택 데모
    print("\n3. Next Greater Elements:")
    arr = [3, 5, 2, 7, 1]
    result = next_greater_indices(arr)
    print(f"Array: {arr}")
    print(f"Next greater indices: {result}")

def demo_graph_algorithms():
    print("\n=== 그래프 알고리즘 데모 ===")
    
    # BFS 데모
    print("\n1. BFS:")
    edges = [(1, 2), (2, 3), (3, 4), (1, 4)]
    graph = build_graph(4, edges, directed=False, one_indexed=True)
    distances = bfs_graph(4, graph, 1, one_indexed=True)
    print(f"Edges: {edges}")
    print(f"Distances from vertex 1: {distances[1:]}")  # Skip index 0
    
    # Dijkstra 데모
    print("\n2. Dijkstra:")
    weighted_graph = [
        [],                    # 0 (unused)
        [(2, 1), (3, 4)],     # 1 -> 2(weight 1), 3(weight 4)  
        [(3, 2), (4, 1)],     # 2 -> 3(weight 2), 4(weight 1)
        [(4, 3)],             # 3 -> 4(weight 3)
        []                    # 4
    ]
    distances = dijkstra(4, weighted_graph, 1, one_indexed=True)
    print(f"Shortest distances from vertex 1: {distances[1:]}")

def demo_tree_structures():
    print("\n=== 트리 자료구조 데모 ===")
    
    # Segment Tree 데모
    print("\n1. Segment Tree (Sum):")
    arr = [1, 2, 3, 4, 5]
    st = SegTreeSum(arr)
    print(f"Array: {arr}")
    print(f"Sum[0,2]: {st.query(0, 2)}")  # 1+2+3=6
    print(f"Sum[1,4]: {st.query(1, 4)}")  # 2+3+4+5=14
    
    st.update(2, 10)  # Change arr[2] from 3 to 10
    print(f"After update arr[2]=10:")
    print(f"Sum[0,2]: {st.query(0, 2)}")  # 1+2+10=13
    
    # Fenwick Tree 데모
    print("\n2. Fenwick Tree:")
    bit = FenwickTree(5)
    for i in range(1, 6):
        bit.add(i, i)  # Add value i at position i
    
    print(f"Prefix sum[1,3]: {bit.sum(3)}")      # 1+2+3=6
    print(f"Range sum[2,4]: {bit.range_sum(2, 4)}")  # 2+3+4=9

def demo_string_algorithms():
    print("\n=== 문자열 알고리즘 데모 ===")
    
    # KMP 데모
    print("\n1. KMP Pattern Matching:")
    text = "ababcababa"
    pattern = "aba"
    positions = kmp_search(text, pattern)
    print(f"Text: '{text}'")
    print(f"Pattern: '{pattern}'")
    print(f"Found at positions: {positions}")
    
    # Trie 데모
    print("\n2. Trie:")
    trie = Trie()
    words = ["cat", "car", "card", "care", "careful"]
    
    for word in words:
        trie.insert(word)
    
    print(f"Inserted words: {words}")
    print(f"Search 'car': {trie.search('car')}")
    print(f"Search 'cart': {trie.search('cart')}")
    print(f"Words with prefix 'car': {trie.count_words_with_prefix('car')}")

def main():
    print("🚀 BOJ Bible 라이브러리 데모")
    print("=" * 50)
    
    demo_basic_structures()
    demo_graph_algorithms()
    demo_tree_structures()
    demo_string_algorithms()
    
    print("\n" + "=" * 50)
    print("✅ 모든 데모 완료!")
    print("\n📚 더 많은 기능은 각 모듈의 문서를 참고하세요.")

if __name__ == "__main__":
    main()