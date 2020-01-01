from math import prod
from typing import List, Iterable

from libaoc.algo import sorted_search
from libaoc.parsers import parse_integer_list


def split_load_in_3(packages: Iterable[int]):
    set_sizes = frozenset(packages)
    sorted_sizes = list(sorted(set_sizes))
    assert sum(set_sizes) % 3 == 0
    target_load = sum(set_sizes) // 3

    for n in range(1, 1 + len(sorted_sizes)):
        for g1 in make_combinations(sorted_sizes, n, target_load):
            set_rem = set_sizes - set(g1)
            sorted_rem = list(sorted(set_rem))
            if g2 := can_make_two_groups(sorted_rem, target_load):
                g3 = tuple(set_rem - set(g2))
                yield g1, g2, g3


def split_load_in_4(packages: List[int]):
    set_sizes = frozenset(packages)
    sorted_sizes = list(sorted(packages))
    assert sum(set_sizes) % 4 == 0
    target_load = sum(set_sizes) // 4

    for n in range(1, 1 + len(packages)):
        for g1 in make_combinations(sorted_sizes, n, target_load):
            set_rem = set_sizes - set(g1)
            if gs := next(split_load_in_3(set_rem), ()):
                yield g1, *gs


def smallest_groups_entanglements(groups):
    lowest_size = 0
    for group, *_ in groups:
        if not lowest_size:
            lowest_size = len(group)
        elif len(group) > lowest_size:
            return
        yield prod(group)


def part_1(packages: List[int]):
    return min(smallest_groups_entanglements(split_load_in_3(packages)))

def part_2(packages: List[int]):
    return min(smallest_groups_entanglements(split_load_in_4(packages)))


def can_make_two_groups(sorted_sizes: List[int], size: int):
    for n in range(1, 2 + len(sorted_sizes) // 2):
        groups = make_combinations(sorted_sizes, n, size)
        if g := next(groups, ()):
            return g
    return ()

def make_combinations(sorted_sizes: List[int], n: int, size: int):
    if n <= 0:
        raise ValueError
    if n == 1:
        if sorted_search(sorted_sizes, size):
            yield (size,)
        return
    for i in reversed(range(len(sorted_sizes))):
        elem = sorted_sizes[i]
        for combination in make_combinations(sorted_sizes[:i], n - 1, size - elem):
            yield combination + (elem,)


def main(data: str):
    packages = parse_integer_list(data)
    yield part_1(packages)
    yield part_2(packages)
