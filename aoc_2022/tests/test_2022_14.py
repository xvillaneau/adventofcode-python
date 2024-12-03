import numpy as np

from aoc_2022 import day_14


EXAMPLE = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

def test_make_cave():
    rocks = day_14.parse_input(EXAMPLE)
    cave = day_14.Cave(rocks)
    assert cave.x_min == 494
    assert cave.x_max == 503
    assert cave.y_max == 9

    assert np.sum(cave.cave == 1) == 20


def test_fall_sand():
    rocks = day_14.parse_input(EXAMPLE)
    cave = day_14.Cave(rocks)

    res = cave.fall_sand()
    assert res is True
    assert cave.sand == 1
    assert cave[500, 8] == 2

    res = cave.fall_sand()
    assert res is True
    assert cave.sand == 2
    assert cave[499, 8] == 2
    assert cave[501, 8] == 0

    while cave.fall_sand():
        continue

    assert cave.sand == 24

    res = cave.fall_sand(part_2=True)
    assert res is True

    while cave.fall_sand(part_2=True):
        pass

    assert cave.sand == 93
