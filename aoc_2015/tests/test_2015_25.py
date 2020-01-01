from aoc_2015.day_25 import index_of

def test_index_of():
    assert index_of(1, 1) == 1
    assert index_of(2, 1) == 2
    assert index_of(1, 2) == 3
    assert index_of(4, 2) == 12
    assert index_of(1, 5) == 15
    assert index_of(6, 1) == 16
