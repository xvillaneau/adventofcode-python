
from aoc_2024 import day_01

EXAMPLE = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

def test_2024_day1_part1():
    l1, l2 = day_01.parse_input(EXAMPLE)
    assert day_01.part_1(l1, l2) == 11


def test_2024_day1_part2():
    l1, l2 = day_01.parse_input(EXAMPLE)
    assert day_01.part_2(l1, l2) == 31
