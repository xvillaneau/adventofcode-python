from aoc_2020.day_23 import *


def test_simple_play():
    assert labels([8, 3, 7, 4, 1, 9, 2, 6, 5]) == "92658374"
    assert labels(play([3, 8, 9, 1, 2, 5, 4, 6, 7])) == "67384529"


def test_many():
    cups = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    cups.extend(range(10, 100_001))
    play(cups, rounds=100_000)
