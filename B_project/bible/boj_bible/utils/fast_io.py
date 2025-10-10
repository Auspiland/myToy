# -*- coding: utf-8 -*-
"""
Fast I/O utilities and common constants for competitive programming
"""

import sys
import math
from typing import List, Tuple, Dict, Set, Optional, Iterable

# Fast I/O setup
input = sys.stdin.readline
INF = 10 ** 18

def read_int() -> int:
    """Read single integer"""
    return int(input())

def read_ints() -> List[int]:
    """Read multiple integers from a line"""
    return list(map(int, input().split()))

def read_string() -> str:
    """Read string (stripped)"""
    return input().strip()

def read_strings() -> List[str]:
    """Read multiple strings from a line"""
    return input().split()

def set_recursion_limit(limit: int = 10**6):
    """Set recursion limit for deep recursion algorithms"""
    sys.setrecursionlimit(limit)

# Common constants
MOD = 10**9 + 7
MOD2 = 998244353
EPS = 1e-9