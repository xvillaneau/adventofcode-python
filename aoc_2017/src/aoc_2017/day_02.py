from typing import Iterable, List
from itertools import combinations


def checksum(table: Iterable[List[int]]):
    return sum(max(row) - min(row) for row in table)


def evenly_divisible(row: List[int]):
    return next(
        max(a, b) // min(a, b) for a, b in combinations(row, 2)
        if max(a, b) % min(a, b) == 0)


def checksum_2(table: Iterable[List[int]]):
    return sum(evenly_divisible(row) for row in table)


if __name__ == "__main__":
    from libaoc import simple_main, files
    simple_main(2017, 2, files.read_int_table, checksum, checksum_2)
