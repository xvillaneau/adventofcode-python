from aoc_2020.day_03 import count_trees, count_all_slopes

EXAMPLE = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""".strip()


def test_part_1():
    assert count_trees(EXAMPLE.splitlines(), 3, 1) == 7


def test_part_2():
    assert count_all_slopes(EXAMPLE.splitlines()) == 336
