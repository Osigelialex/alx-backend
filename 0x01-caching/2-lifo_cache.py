#!/usr/bin/env python3
"""A module for implementing LIFO Caching
"""
from base_caching import BaseCaching
from typing import Union


class LIFOCache(BaseCaching):
    """A class for LIFO Caching
    """
    def __init__(self) -> None:
        """Initializes cache in parent
        """
        super().__init__()

    def put(self, key: str, item: str) -> None:
        """sets key with item in cache
        """
        if key is None or item is None:
            return

        # discard last item if cache is full
        if len(self.cache_data) > super().MAX_ITEMS:
            index = list(self.cache_data)[-1]
            self.cache_data.pop(index)
            print("DISCARD: {}".format(index))

        # set key in cache
        self.cache_data[key] = item

    def get(self, key: str) -> Union[str, None]:
        """retrieves key from cache
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
