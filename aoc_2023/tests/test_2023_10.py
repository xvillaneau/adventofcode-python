import pytest

from aoc_2023 import day_10

EXAMPLE_1 = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""
EXAMPLE_2 = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""
EXAMPLE_3 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""
EXAMPLE_4 = """
FF7F7F7F7F7F7F7F---7
L|LJS|||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""


@pytest.mark.parametrize("data,start_pos,start_pipe", [
    (EXAMPLE_1, (1, 3), "F"),
    (EXAMPLE_2, (0, 2), "F"),
])
def test_setup_start(data, start_pos, start_pipe):
    grid = day_10.load_grid(data)
    start = day_10.setup_start(grid)
    assert start == start_pos
    assert grid[*start_pos] == start_pipe


@pytest.mark.parametrize("data,length", [
    (EXAMPLE_1, 8),
    (EXAMPLE_2, 16),
])
def test_setup_start(data, length):
    grid = day_10.load_grid(data)
    start = day_10.setup_start(grid)
    assert day_10.follow_loop(grid, start) == length


@pytest.mark.parametrize("data,tiles", [
    (EXAMPLE_3, 8),
    (EXAMPLE_4, 10),
])
def test_main(data, tiles):
    res = list(day_10.main(data))
    assert res[1] == tiles
