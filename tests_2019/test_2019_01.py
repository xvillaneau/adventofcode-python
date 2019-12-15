from aoc_2019.day_01 import fuel_required, adjusted_fuel

def test_fuel_required():
    assert fuel_required(12) == 2
    assert fuel_required(14) == 2
    assert fuel_required(1969) == 654
    assert fuel_required(100756) == 33583

def test_adjusted_fuel():
    assert adjusted_fuel(14) == 2
    assert adjusted_fuel(1969) == 966
    assert adjusted_fuel(100756) == 50346