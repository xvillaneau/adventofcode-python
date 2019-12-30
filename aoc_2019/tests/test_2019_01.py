from aoc_2019.day_01 import AocRunner

runner = AocRunner().run


def test_fuel_required():
    assert tuple(runner([12])) == (2, 2)
    assert tuple(runner([14])) == (2, 2)
    assert tuple(runner([1969])) == (654, 966)
    assert tuple(runner([100756])) == (33583, 50346)
