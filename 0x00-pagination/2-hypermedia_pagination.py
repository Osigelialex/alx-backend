#!/usr/bin/env python3
"""A module for simple pagination"""
import csv
import math
from typing import List, Dict
from itertools import islice

index_range = __import__('0-simple_helper_function').index_range


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "./Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """returns appropriate page from dataset"""
        assert(isinstance(page, int))
        assert(isinstance(page_size, int))
        assert(page > 0)
        assert(page_size > 0)

        content = []
        start, end = index_range(page, page_size)

        with open(Server.DATA_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in islice(reader, start, end):
                content.append(row)

        return content

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """perfoms hypermedia pagination on dataset"""
        requested_page = self.get_page(page, page_size)
        page_count = math.floor(19419 / page_size)

        # check if page is valid
        if page > page_count:
            page_size = 0

        next_page = page + 1 if page < page_count else None
        prev_page = page - 1 if page > 0 else None

        return {
            'page_size': page_size,
            'page': page,
            'data': requested_page,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': page_count
        }
