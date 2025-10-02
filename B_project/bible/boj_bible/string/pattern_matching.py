# -*- coding: utf-8 -*-
"""
String pattern matching algorithms: KMP, Z-algorithm, etc.
"""

from typing import List

def compute_lps(pattern: str) -> List[int]:
    """
    Compute Longest Proper Prefix which is also Suffix array for KMP
    
    Args:
        pattern: Pattern string
        
    Returns:
        LPS array
        
    Time: O(m), Space: O(m)
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    KMP pattern matching algorithm
    
    Args:
        text: Text to search in
        pattern: Pattern to search for
        
    Returns:
        List of starting positions where pattern is found
        
    Time: O(n + m), Space: O(m)
    """
    if not pattern:
        return []
    
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    
    positions = []
    i = j = 0
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return positions

def z_algorithm(s: str) -> List[int]:
    """
    Z-algorithm for finding all substrings that match prefix
    
    Args:
        s: Input string
        
    Returns:
        Z array where z[i] is length of longest substring starting from i
        which is also a prefix of s
        
    Time: O(n), Space: O(n)
    """
    n = len(s)
    z = [0] * n
    l = r = 0
    
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    
    return z

def pattern_match_z(text: str, pattern: str) -> List[int]:
    """
    Pattern matching using Z-algorithm
    
    Args:
        text: Text to search in
        pattern: Pattern to search for
        
    Returns:
        List of starting positions where pattern is found
        
    Time: O(n + m), Space: O(n + m)
    """
    if not pattern:
        return []
    
    combined = pattern + "#" + text
    z = z_algorithm(combined)
    
    positions = []
    pattern_len = len(pattern)
    
    for i in range(pattern_len + 1, len(combined)):
        if z[i] == pattern_len:
            positions.append(i - pattern_len - 1)
    
    return positions

def manacher_algorithm(s: str) -> List[int]:
    """
    Manacher's algorithm for finding all palindromic substrings
    
    Args:
        s: Input string
        
    Returns:
        Array where result[i] is radius of longest palindrome centered at i
        in the processed string (with separators)
        
    Time: O(n), Space: O(n)
    """
    # Preprocess string: "abc" -> "^#a#b#c#$"
    processed = "^#" + "#".join(s) + "#$"
    n = len(processed)
    radius = [0] * n
    center = right = 0
    
    for i in range(1, n - 1):
        mirror = 2 * center - i
        
        if i < right:
            radius[i] = min(right - i, radius[mirror])
        
        # Try to expand palindrome centered at i
        while processed[i + radius[i] + 1] == processed[i - radius[i] - 1]:
            radius[i] += 1
        
        # If palindrome centered at i extends past right, adjust center and right
        if i + radius[i] > right:
            center, right = i, i + radius[i]
    
    return radius

def longest_palindromic_substring(s: str) -> str:
    """
    Find longest palindromic substring using Manacher's algorithm
    
    Args:
        s: Input string
        
    Returns:
        Longest palindromic substring
        
    Time: O(n), Space: O(n)
    """
    if not s:
        return ""
    
    radius = manacher_algorithm(s)
    
    # Find the longest palindrome
    max_radius = 0
    center_index = 0
    
    for i in range(len(radius)):
        if radius[i] > max_radius:
            max_radius = radius[i]
            center_index = i
    
    # Convert back to original string coordinates
    start = (center_index - max_radius) // 2
    length = max_radius
    
    return s[start:start + length]

def rolling_hash(s: str, base: int = 31, mod: int = 10**9 + 7) -> List[int]:
    """
    Compute rolling hash for all prefixes
    
    Args:
        s: Input string
        base: Base for rolling hash
        mod: Modulo for rolling hash
        
    Returns:
        List of prefix hashes
        
    Time: O(n), Space: O(n)
    """
    n = len(s)
    hash_values = [0] * (n + 1)
    
    for i in range(n):
        hash_values[i + 1] = (hash_values[i] * base + ord(s[i])) % mod
    
    return hash_values

def substring_hash(hash_values: List[int], powers: List[int], 
                  l: int, r: int, mod: int = 10**9 + 7) -> int:
    """
    Get hash of substring s[l:r+1] using precomputed values
    
    Args:
        hash_values: Precomputed prefix hashes
        powers: Precomputed powers of base
        l, r: Substring boundaries (0-indexed)
        mod: Modulo for rolling hash
        
    Returns:
        Hash of substring s[l:r+1]
        
    Time: O(1), Space: O(1)
    """
    return (hash_values[r + 1] - hash_values[l] * powers[r - l + 1]) % mod

def precompute_powers(n: int, base: int = 31, mod: int = 10**9 + 7) -> List[int]:
    """
    Precompute powers of base for rolling hash
    
    Args:
        n: Maximum length needed
        base: Base for rolling hash
        mod: Modulo for rolling hash
        
    Returns:
        List of powers: [base^0, base^1, ..., base^n]
        
    Time: O(n), Space: O(n)
    """
    powers = [1] * (n + 1)
    for i in range(1, n + 1):
        powers[i] = (powers[i - 1] * base) % mod
    return powers