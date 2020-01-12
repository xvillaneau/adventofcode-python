from aoc_2018.day_18 import *

EXAMPLE_0 = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""".strip()

EXAMPLE_1 = """
.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.
""".strip()


def test_load():
    assert repr_area(parse_input(EXAMPLE_0)) == EXAMPLE_0


def test_transform():
    area = parse_input(EXAMPLE_0)
    assert repr_area(transform(area)) == EXAMPLE_1


def test_value_after():
    area = parse_input(EXAMPLE_0)
    assert value_after(area, 10) == 1147
