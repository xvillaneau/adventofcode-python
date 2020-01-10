from aoc_2018.day_08 import metadata_sum, metadata_value

EXAMPLE = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def test_metadata_sum():
    assert metadata_sum(EXAMPLE) == 138


def test_metadata_value():
    assert metadata_value(EXAMPLE) == 66
