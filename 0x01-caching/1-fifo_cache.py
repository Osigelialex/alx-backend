#!/usr/bin/env python3
"""A module for implementing FIFO caching
"""
from typing import Union
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """Fifo cache class
    """
    def __init__(self):
        """initializes cache dict in parent
        """
        super().__init__()

    def put(self, key: str, item: str) -> None:
        """assigns key to item in cache
        """
        if key is None or item is None:
            return

        # discard first item if max size if reached
        if len(self.cache_data) == super().MAX_ITEMS:
            index = next(iter(self.cache_data))
            del self.cache_data[index]
            print("DISCARD: {}".format(index))

        # assign key to item in cache
        self.cache_data[key] = item

    def get(self, key: str) -> Union[str, None]:
        """gets key value from cache
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
