#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """returns items from dataset despite page drift
        """
        # get index of last item
        row_count = len(self.dataset())
        max_pages = math.floor(row_count / page_size)

        # check that index is valid
        assert(index < row_count)

        # calculate page
        page = math.floor(index / page_size)

        # calculate indexes
        start_index = page * page_size + 1
        last_index = start_index + page_size - 1

        # get datasets
        indexed_dataset = self.indexed_dataset()
        dataset = self.dataset()

        # create requested dataset
        requested_dataset = []

        # get sorted keys
        keys = list(indexed_dataset)

        # calculate indexes after page_drift
        next_index = min(last_index + 1, len(dataset))

        # read dataset
        for i in range(keys[start_index], keys[next_index]):
            key = keys[i]

            # check if key was deleted
            if dataset[i] != indexed_dataset.get(key):
                # use indexed dataset to get correct value
                requested_dataset.append(indexed_dataset.get(key))
            else:
                # use unindexed dataset to get correct value
                requested_dataset.append(dataset[i])

        return {
            "index": start_index,
            "next_index": next_index,
            "page_size": page_size,
            "data": requested_dataset
        }
