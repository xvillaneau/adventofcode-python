from aoc_2024 import day_06

EXAMPLE = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


def test_parse_input():
    lab, start = day_06.parse_input(EXAMPLE)

    assert lab.shape == (10, 10)
    assert start == (6, 4)


def test_main():
    part_1, part_2 = day_06.main(EXAMPLE)

    assert part_1 == 41
    assert part_2 == 6
