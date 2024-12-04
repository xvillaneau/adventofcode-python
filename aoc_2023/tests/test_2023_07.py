from more_itertools import windowed
import pytest

from aoc_2023 import day_07


EXAMPLE = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".strip()

TEST_ORDER = """
AAAAA
TTTTT
88888
AA8AA
T2222
23332
222AA
TTT98
5AA2A
23432
232A3
A23A4
23AQ3
23456
""".strip()


@pytest.mark.parametrize("greater,lower", windowed(TEST_ORDER.splitlines(), 2))
def test_hand_order(greater, lower):
    assert day_07.hand_order(greater) > day_07.hand_order(lower)


def test_main():
    res = list(day_07.main(EXAMPLE))
    assert res == [6440, 5905]
