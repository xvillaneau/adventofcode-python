from aoc_2015.day_24 import split_load_in_3

def test_part_1():
    sizes = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
    assert split_load_in_3(sizes) == 99
