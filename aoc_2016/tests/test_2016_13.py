from aoc_2016.day_13 import shortest_path, Pos, count_reachable

def test_shortest_path():
    assert shortest_path(10, Pos(7, 4)) == 11

def test_count_reachable():
    assert count_reachable(10, 5) == 11
