import numpy as np
import pytest

from aoc_2021.day_20 import parse_data, enhance

EXAMPLE = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


def test_parse_data():
    alg, mat = parse_data(EXAMPLE)
    assert alg.shape == (512,)
    assert all(alg[:5] == [False, False, True, False, True])
    assert mat.shape == (5, 5)
    assert mat[0, 0] == 1


def test_enhance():
    alg, mat = parse_data(EXAMPLE)
    mat, fill = enhance(alg, mat, False)
    assert mat.shape == (7, 7)
    assert all(mat[0] == [0, 1, 1, 0, 1, 1, 0])
    assert fill == 0


COUNTS = [(2, 35), (50, 3351)]


@pytest.mark.parametrize("steps,count", COUNTS)
def test_enhance_many(steps, count):
    alg, mat = parse_data(EXAMPLE)
    fill = False
    for _ in range(steps):
        mat, fill = enhance(alg, mat, fill)
    assert np.sum(mat) == count
