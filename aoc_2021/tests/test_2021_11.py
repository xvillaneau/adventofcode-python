import numpy as np

from aoc_2021.day_11 import octopus_step, count_flashes, detect_sync
from libaoc.parsers import parse_digit_matrix

EXAMPLE = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""


def test_octopus_step():
    levels_0 = parse_digit_matrix("11111\n19991\n19191\n19991\n11111")
    levels_1 = parse_digit_matrix("34543\n40004\n50005\n40004\n34543")
    levels_2 = parse_digit_matrix("45654\n51115\n61116\n51115\n45654")

    res_1, n_1 = octopus_step(levels_0)
    assert n_1 == 9
    assert np.all(res_1 == levels_1)

    res_2, n_2 = octopus_step(levels_1)
    assert n_2 == 0
    assert np.all(res_2 == levels_2)


def test_count_flashes():
    levels = parse_digit_matrix(EXAMPLE)
    assert count_flashes(levels, 10) == 204
    assert count_flashes(levels, 100) == 1656


def test_detect_sync():
    levels = parse_digit_matrix(EXAMPLE)
    assert detect_sync(levels) == 195
