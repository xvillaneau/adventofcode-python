import pytest
from aoc_2018.day_11 import make_power_levels

GRID_TESTS = [(8, 3, 5, 4), (57, 122, 79, -5), (39, 217, 196, 0), (71, 101, 153, 4)]


@pytest.mark.parametrize("sn,x,y,level", GRID_TESTS)
def test_gen_powers(sn, x, y, level):
    power_levels = make_power_levels(sn)
    assert power_levels[x - 1, y - 1] == level
