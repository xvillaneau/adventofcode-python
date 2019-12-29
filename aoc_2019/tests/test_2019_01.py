from aoc_2019.day_01 import fuel_iter


def test_fuel_required():
    assert next(fuel_iter(12)) == 2
    assert next(fuel_iter(14)) == 2
    assert next(fuel_iter(1969)) == 654
    assert next(fuel_iter(100756)) == 33583


def test_adjusted_fuel():
    assert sum(fuel_iter(14)) == 2
    assert sum(fuel_iter(1969)) == 966
    assert sum(fuel_iter(100756)) == 50346
