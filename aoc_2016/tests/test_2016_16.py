from itertools import islice

from aoc_2016.day_16 import dragon_iter, compute_checksum


def test_dragon_iter():
    assert "".join(islice(dragon_iter("0"), 3)) == "001"
    assert "".join(islice(dragon_iter("1"), 3)) == "100"
    assert "".join(islice(dragon_iter("1"), 7)) == "1000110"
    assert "".join(islice(dragon_iter("1"), 15)) == "100011001001110"


def test_compute_checksum():
    assert compute_checksum("1100101101", 12) == "100"
    assert compute_checksum("10000", 20) == "01100"
