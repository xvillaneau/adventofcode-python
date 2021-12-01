from aoc_2021.day_01 import count_increases, count_three_increases

DEPTHS = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]


def test_count_increases():
    assert count_increases(DEPTHS) == 7


def test_three_count_increases():
    assert count_three_increases(DEPTHS) == 5
