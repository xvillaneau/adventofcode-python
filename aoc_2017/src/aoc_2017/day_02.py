from typing import Iterable, List
from itertools import combinations

from libaoc.parsers import parse_integer_table


def checksum(table: Iterable[List[int]]):
    return sum(max(row) - min(row) for row in table)


def evenly_divisible(row: List[int]):
    return next(
        max(a, b) // min(a, b) for a, b in combinations(row, 2)
        if max(a, b) % min(a, b) == 0)


def checksum_2(table: Iterable[List[int]]):
    return sum(evenly_divisible(row) for row in table)


def main(data: str):
    table = parse_integer_table(data)
    yield checksum(table)
    yield checksum_2(table)
