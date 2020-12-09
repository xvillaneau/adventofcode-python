from aoc_2020.day_09 import find_invalid, find_weakness

EXAMPLE = [
    35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127,
    219, 299, 277, 309, 576
]


def test_find_invalid():
    assert find_invalid(EXAMPLE, buffer=5) == 127


def test_find_weakness():
    assert find_weakness(EXAMPLE, 127) == 62
