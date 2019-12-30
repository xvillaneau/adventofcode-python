import numpy as np
from libaoc.matrix import load_string_matrix
from aoc_2019.day_24 import (
    load_bugs,
    step,
    biodiversity,
    first_repeat,
    count_after_n_steps,
)

EXAMPLE = """
....#
#..#.
#..##
..#..
#....
"""

EXAMPLE_STEP_1 = """
#..#.
####.
###.#
##.##
.##..
"""

EXAMPLE_STEP_2 = """
#####
....#
....#
...#.
#.###
"""

EXAMPLE_REPEAT = """
.....
.....
.....
#....
.#...
"""


def test_step():
    b0 = load_bugs(EXAMPLE)
    b1 = step(b0)
    assert np.all(b1 == load_bugs(EXAMPLE_STEP_1))
    b2 = step(b1)
    assert np.all(b2 == load_bugs(EXAMPLE_STEP_2))


def test_biodiversity():
    assert biodiversity(load_bugs(EXAMPLE)) == 0b100100110010100110000
    assert biodiversity(load_bugs(EXAMPLE_REPEAT)) == 2129920


def test_first_repeat():
    assert first_repeat(load_bugs(EXAMPLE)) == 2129920


def test_count_after_n_steps():
    assert count_after_n_steps(load_bugs(EXAMPLE), 10) == 99
