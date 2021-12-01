from libaoc.parsers import parse_integer_list

from more_itertools import windowed


def count_increases(depths: list[int]) -> int:
    return sum(a < b for a, b in windowed(depths, 2))


def count_three_increases(depths: list[int]) -> int:
    return sum(a < d for a, _, _, d in windowed(depths, 4))


def main(data: str):
    depths = parse_integer_list(data)
    yield count_increases(depths)
    yield count_three_increases(depths)
