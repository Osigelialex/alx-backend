#!/usr/bin/env python3
"""A basic cache module
"""
from base_caching import BaseCaching
from typing import Union


class BasicCache(BaseCaching):
    """Class implements a basic cache
    """
    def __init__(self) -> None:
        """Initializes the cache_data dict in parent class
        """
        super().__init__()

    def put(self, key: Union[str, None], item: Union[str, None]) -> None:
        """set key with item value in cache
        """
        if key is None or item is None:
            return

        self.cache_data[key] = item

    def get(self, key: str) -> Union[str, None]:
        """retrieves key value from cache
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
