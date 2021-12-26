import numpy as np
import pytest

from aoc_2021.day_25 import step, steps_to_static
from libaoc.matrix import load_string_matrix


EXAMPLE_1_0 = "...>>>>>..."
EXAMPLE_1_1 = "...>>>>.>.."
EXAMPLE_1_2 = "...>>>.>.>."
EXAMPLE_2_0 = """
..........
.>v....v..
.......>..
..........
"""
EXAMPLE_2_1 = """
..........
.>........
..v....v>.
..........
"""
EXAMPLE_3_0 = """
...>...
.......
......>
v.....>
......>
.......
..vvv..
"""
EXAMPLE_3_1 = """
..vv>..
.......
>......
v.....>
>......
.......
....v..
"""
EXAMPLE_3_2 = """
....v>.
..vv...
.>.....
......>
v>.....
.......
.......
"""
EXAMPLE_3_3 = """
......>
..v.v..
..>v...
>......
..>....
v......
.......
"""
EXAMPLE_3_4 = """
>......
..v....
..>.v..
.>.v...
...>...
.......
v......
"""
STEP_TESTS = [
    (EXAMPLE_1_0, EXAMPLE_1_1),
    (EXAMPLE_1_1, EXAMPLE_1_2),
    (EXAMPLE_2_0, EXAMPLE_2_1),
    (EXAMPLE_3_0, EXAMPLE_3_1),
    (EXAMPLE_3_1, EXAMPLE_3_2),
    (EXAMPLE_3_2, EXAMPLE_3_3),
    (EXAMPLE_3_3, EXAMPLE_3_4),
]


@pytest.mark.parametrize("before,after", STEP_TESTS)
def test_step(before, after):
    before = load_string_matrix(before)
    after = load_string_matrix(after)
    assert np.all(step(before)[0] == after)


EXAMPLE = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""


def test_steps_to_static():
    cucumbers = load_string_matrix(EXAMPLE)
    assert steps_to_static(cucumbers) == 58
