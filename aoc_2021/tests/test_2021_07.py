from aoc_2021.day_07 import find_low_fuel_1, find_low_fuel_2

EXAMPLE = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]

def test_find_low_fuel_1():
    assert find_low_fuel_1(EXAMPLE) == 37

def test_find_low_fuel_2():
    assert find_low_fuel_2(EXAMPLE) == 168
