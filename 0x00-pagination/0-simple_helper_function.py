#!/usr/bin/env python3
"""
A module for calculating the range of indexes to return in
a list for those particular pagination parameters
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """caculates the range of indexes"""
    start = 0 if page == 1 else page_size * (page - 1)
    end = page_size * page
    return (start, end)
