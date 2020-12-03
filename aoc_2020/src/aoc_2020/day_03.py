from math import prod
from typing import List


def count_trees(pattern: List[str], right: int, down: int):
    pos, count, size = 0, 0, len(pattern[0])

    for row in pattern[::down]:
        count += (row[pos] == "#")
        pos = (pos + right) % size

    return count


def count_all_slopes(pattern: List[str]):
    return prod([
        count_trees(pattern, 1, 1),
        count_trees(pattern, 3, 1),
        count_trees(pattern, 5, 1),
        count_trees(pattern, 7, 1),
        count_trees(pattern, 1, 2),
    ])


def main(data: str):
    pattern = data.splitlines()
    yield count_trees(pattern, 3, 1)
    yield count_all_slopes(pattern)
