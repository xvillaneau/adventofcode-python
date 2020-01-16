from textwrap import dedent
import pytest
from aoc_2018.day_25 import *

EXAMPLES = [
    (
        dedent(
            """
            0,0,0,0
            3,0,0,0
            0,3,0,0
            0,0,3,0
            0,0,0,3
            0,0,0,6
            9,0,0,0
            12,0,0,0
            """
        ).lstrip(),
        2,
    ),
]


@pytest.mark.parametrize("data,n", EXAMPLES)
def test_count_constellations(data, n):
    assert count_constellations(data) == n
