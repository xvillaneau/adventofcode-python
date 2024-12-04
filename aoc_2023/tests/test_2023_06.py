import pytest

from aoc_2023 import day_06

EXAMPLE = """
Time:      7  15   30
Distance:  9  40  200
"""


@pytest.mark.parametrize("time,distance,expected", [(7, 9, 4), (15, 40, 8), (30, 200, 9)])
def test_ways_to_win(time, distance, expected):
    assert day_06.ways_to_win(time, distance) == expected


def test_main():
    res = list(day_06.main(EXAMPLE))
    assert res[0] == 288
    assert res[1] == 71503
