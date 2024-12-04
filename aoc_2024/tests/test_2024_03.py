
from aoc_2024 import day_03

EXAMPLE_1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
EXAMPLE_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def test_parse_mem():
    assert day_03.parse_mem(EXAMPLE_1) == [8, 25, 88, 40]
    assert day_03.parse_mem(EXAMPLE_2) == [8, day_03.DONT, 25, 88, day_03.DO, 40]


def test_part_1():
    tokens = day_03.parse_mem(EXAMPLE_1)
    p1, _ = day_03.sum_mul(tokens)
    assert p1 == 161


def test_part_2():
    tokens = day_03.parse_mem(EXAMPLE_2)
    _, p2 = day_03.sum_mul(tokens)
    assert p2 == 48
