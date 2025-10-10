# -*- coding: utf-8 -*-
"""
String algorithms module
"""

from .pattern_matching import (
    compute_lps, kmp_search, z_algorithm, pattern_match_z,
    manacher_algorithm, longest_palindromic_substring,
    rolling_hash, substring_hash, precompute_powers
)
from .trie import Trie, TrieNode, BinaryTrie

__all__ = [
    # Pattern matching
    'compute_lps', 'kmp_search', 'z_algorithm', 'pattern_match_z',
    'manacher_algorithm', 'longest_palindromic_substring',
    'rolling_hash', 'substring_hash', 'precompute_powers',
    
    # Trie
    'Trie', 'TrieNode', 'BinaryTrie'
]