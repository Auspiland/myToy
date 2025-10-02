# -*- coding: utf-8 -*-
"""
String algorithm tests
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boj_bible.string.pattern_matching import kmp_search, z_algorithm, longest_palindromic_substring
from boj_bible.string.trie import Trie


class TestKMP(unittest.TestCase):
    def test_kmp_search(self):
        text = "ababcababa"
        pattern = "aba"
        
        positions = kmp_search(text, pattern)
        expected = [0, 2, 5, 7]  # All positions where "aba" occurs
        self.assertEqual(positions, expected)
        
        # Test with no matches
        positions = kmp_search("hello", "world")
        self.assertEqual(positions, [])
        
        # Test with empty pattern
        positions = kmp_search("hello", "")
        self.assertEqual(positions, [])


class TestZAlgorithm(unittest.TestCase):
    def test_z_algorithm(self):
        s = "ababaca"
        z = z_algorithm(s)
        
        # z[i] = length of longest substring starting from i that is also prefix
        self.assertEqual(z[0], 0)  # By convention
        self.assertEqual(z[1], 0)  # "babaca" vs "ababaca"
        self.assertEqual(z[2], 3)  # "abaca" vs "ababaca" -> "aba" matches
        self.assertEqual(z[3], 0)  # "baca" vs "ababaca"


class TestManacher(unittest.TestCase):
    def test_longest_palindromic_substring(self):
        # Simple palindrome
        self.assertEqual(longest_palindromic_substring("aba"), "aba")
        
        # Even length palindrome
        self.assertEqual(longest_palindromic_substring("abba"), "abba")
        
        # Longer string with palindrome
        result = longest_palindromic_substring("babad")
        self.assertIn(result, ["bab", "aba"])  # Both are valid
        
        # No palindrome longer than 1
        self.assertEqual(len(longest_palindromic_substring("abcd")), 1)


class TestTrie(unittest.TestCase):
    def test_trie_operations(self):
        trie = Trie()
        
        # Insert words
        words = ["cat", "car", "card", "care", "careful"]
        for word in words:
            trie.insert(word)
        
        # Test search
        self.assertTrue(trie.search("cat"))
        self.assertTrue(trie.search("card"))
        self.assertFalse(trie.search("cart"))
        
        # Test prefix search
        self.assertTrue(trie.starts_with("car"))
        self.assertTrue(trie.starts_with("care"))
        self.assertFalse(trie.starts_with("dog"))
        
        # Test prefix counting
        self.assertEqual(trie.count_words_with_prefix("car"), 4)  # car, card, care, careful
        self.assertEqual(trie.count_words_with_prefix("care"), 2)  # care, careful
        
        # Test getting words with prefix
        car_words = trie.get_all_words_with_prefix("car")
        self.assertEqual(set(car_words), {"car", "card", "care", "careful"})
        
        # Test deletion
        self.assertTrue(trie.delete("card"))
        self.assertFalse(trie.search("card"))
        self.assertTrue(trie.search("car"))  # Should still exist
        
        # Test deleting non-existent word
        self.assertFalse(trie.delete("nonexistent"))


if __name__ == '__main__':
    unittest.main()