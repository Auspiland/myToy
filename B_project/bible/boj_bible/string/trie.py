# -*- coding: utf-8 -*-
"""
Trie (Prefix Tree) implementation and related algorithms
"""

from typing import Dict, List, Optional

class TrieNode:
    """Node for Trie data structure"""
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word = False
        self.count = 0  # Number of words ending at this node

class Trie:
    """
    Trie (Prefix Tree) implementation
    """
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """
        Insert a word into the trie
        
        Args:
            word: Word to insert
            
        Time: O(m), Space: O(m) where m is length of word
        """
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.count += 1
    
    def search(self, word: str) -> bool:
        """
        Search for a word in the trie
        
        Args:
            word: Word to search for
            
        Returns:
            True if word exists in trie
            
        Time: O(m), Space: O(1)
        """
        node = self._find_node(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word starts with given prefix
        
        Args:
            prefix: Prefix to check
            
        Returns:
            True if any word starts with prefix
            
        Time: O(m), Space: O(1)
        """
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Find node corresponding to prefix"""
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def count_words_with_prefix(self, prefix: str) -> int:
        """
        Count number of words with given prefix
        
        Args:
            prefix: Prefix to count
            
        Returns:
            Number of words starting with prefix
            
        Time: O(m + k) where k is number of nodes in subtree
        """
        node = self._find_node(prefix)
        if node is None:
            return 0
        
        return self._count_words_in_subtree(node)
    
    def _count_words_in_subtree(self, node: TrieNode) -> int:
        """Count words in subtree rooted at node"""
        count = node.count
        
        for child in node.children.values():
            count += self._count_words_in_subtree(child)
        
        return count
    
    def get_all_words_with_prefix(self, prefix: str) -> List[str]:
        """
        Get all words with given prefix
        
        Args:
            prefix: Prefix to search for
            
        Returns:
            List of all words starting with prefix
            
        Time: O(m + k) where k is total length of result words
        """
        node = self._find_node(prefix)
        if node is None:
            return []
        
        result = []
        self._dfs_words(node, prefix, result)
        return result
    
    def _dfs_words(self, node: TrieNode, current_word: str, result: List[str]):
        """DFS to collect all words in subtree"""
        if node.is_end_of_word:
            for _ in range(node.count):
                result.append(current_word)
        
        for char, child in node.children.items():
            self._dfs_words(child, current_word + char, result)
    
    def delete(self, word: str) -> bool:
        """
        Delete a word from the trie
        
        Args:
            word: Word to delete
            
        Returns:
            True if word was deleted, False if word didn't exist
            
        Time: O(m), Space: O(m) for recursion
        """
        return self._delete_helper(self.root, word, 0)
    
    def _delete_helper(self, node: TrieNode, word: str, index: int) -> bool:
        """Helper method for deletion"""
        if index == len(word):
            if not node.is_end_of_word:
                return False
            
            node.count -= 1
            if node.count == 0:
                node.is_end_of_word = False
            
            # Return True if current node has no children (can be deleted)
            return len(node.children) == 0 and not node.is_end_of_word
        
        char = word[index]
        child = node.children.get(char)
        
        if child is None:
            return False
        
        should_delete_child = self._delete_helper(child, word, index + 1)
        
        if should_delete_child:
            del node.children[char]
            # Return True if current node has no children and is not end of word
            return len(node.children) == 0 and not node.is_end_of_word
        
        return False
    
    def longest_common_prefix(self) -> str:
        """
        Find longest common prefix of all words in trie
        
        Returns:
            Longest common prefix of all words
            
        Time: O(p) where p is length of longest common prefix
        """
        if not self.root.children:
            return ""
        
        node = self.root
        prefix = ""
        
        while len(node.children) == 1 and not node.is_end_of_word:
            char = next(iter(node.children.keys()))
            prefix += char
            node = node.children[char]
        
        return prefix

class BinaryTrie:
    """
    Binary trie for XOR operations on integers
    """
    def __init__(self, max_bits: int = 32):
        self.root = TrieNode()
        self.max_bits = max_bits
    
    def insert(self, num: int) -> None:
        """
        Insert a number into binary trie
        
        Args:
            num: Number to insert
            
        Time: O(log num), Space: O(log num)
        """
        node = self.root
        
        for i in range(self.max_bits - 1, -1, -1):
            bit = str((num >> i) & 1)
            
            if bit not in node.children:
                node.children[bit] = TrieNode()
            
            node = node.children[bit]
        
        node.is_end_of_word = True
        node.count += 1
    
    def max_xor(self, num: int) -> int:
        """
        Find maximum XOR of num with any number in trie
        
        Args:
            num: Number to find maximum XOR for
            
        Returns:
            Maximum XOR value possible
            
        Time: O(log num), Space: O(1)
        """
        if not self.root.children:
            return 0
        
        node = self.root
        max_xor = 0
        
        for i in range(self.max_bits - 1, -1, -1):
            bit = (num >> i) & 1
            # Try to go in opposite direction for maximum XOR
            opposite_bit = str(1 - bit)
            
            if opposite_bit in node.children:
                max_xor |= (1 << i)
                node = node.children[opposite_bit]
            else:
                node = node.children[str(bit)]
        
        return max_xor