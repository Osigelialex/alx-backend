#!/usr/bin/env python3
"""A module for implementing lru caching
"""
from base_caching import BaseCaching
from typing import Union, Dict


class LRUCache(BaseCaching):
    """LRUCache class
    """
    def __init__(self) -> None:
        """initializes cache
        """
        super().__init__()
        # create age bits to track least recently used item
        self.age_bit: Dict = {}

    def put(self, key: str, item: str) -> None:
        """sets key in cache
        """
        if key is None or item is None:
            return

        # remove least recently used item
        if len(self.cache_data) == super().MAX_ITEMS:
            # get least recently used item
            index = min(self.age_bit, key=lambda k: self.age_bit[k])
            del self.cache_data[index]
            del self.age_bit[index]
            print("DISCARD: {}".format(index))

        self.cache_data[key] = item

        # set age bit count for key
        if key not in self.age_bit:
            self.age_bit[key] = 0
        else:
            self.age_bit[key] = self.age_bit[key] + 1

    def get(self, key: str) -> Union[str, None]:
        """retrieves item from cache
        """
        if key is None or key not in self.cache_data:
            return None

        # update age bit count for key
        self.age_bit[key] = self.age_bit[key] + 1
        return self.cache_data[key]
