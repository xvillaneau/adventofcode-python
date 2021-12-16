from aoc_2021.day_15 import low_risk_path, low_risk_path_5x
from libaoc.parsers import parse_digit_matrix

EXAMPLE = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""


def test_low_risk_path():
    cave = parse_digit_matrix(EXAMPLE)
    assert low_risk_path(cave) == 40


def test_low_risk_path_5x():
    cave = parse_digit_matrix(EXAMPLE)
    assert low_risk_path_5x(cave) == 315
