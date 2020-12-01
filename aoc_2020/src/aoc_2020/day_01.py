from math import prod
from typing import Dict, List, Set, Tuple

from libaoc.parsers import parse_integer_list


def find_2020_sums(expenses: List[int]):
    traversed_1: Set[int] = set()
    traversed_2: Dict[int, Tuple[int, int]] = {}
    prod_1, prod_2 = None, None

    for entry in expenses:
        complement = 2020 - entry

        if prod_1 is None and complement in traversed_1:
            prod_1 = entry * complement
        if prod_2 is None and complement in traversed_2:
            prod_2 = entry * prod(traversed_2[complement])
        if prod_1 is not None and prod_2 is not None:
            break

        for other in traversed_1:
            if other + entry < 2020:
                traversed_2[other + entry] = (other, entry)
        traversed_1.add(entry)

    return prod_1, prod_2


def main(data: str):
    yield from find_2020_sums(parse_integer_list(data))
