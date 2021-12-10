from aoc_2021.day_09 import load_map, find_minima, risk_level, find_basins

EXAMPLE = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
EXAMPLE2 = """
21...43210
3.878.4.21
.85678.8.2
87678.678.
.8...65678
"""

def test_load_map():
    heightmap = load_map(EXAMPLE)
    assert heightmap.shape == (5, 10)
    assert heightmap[0, 0] == 2
    assert heightmap[4, 0] == 9
    assert heightmap[0, 9] == 0


def test_find_minima():
    heightmap = load_map(EXAMPLE)
    minima = find_minima(heightmap)
    assert len(minima) == 4
    assert set(minima) == {(0, 1), (0, 9), (2, 2), (4, 6)}


def test_risk_level():
    heightmap = load_map(EXAMPLE)
    assert risk_level(heightmap) == 15


def test_find_basins():
    heightmap = load_map(EXAMPLE)
    assert find_basins(heightmap) == 1134
