import numpy as np

from aoc_2022 import day_08
from libaoc.parsers import parse_digit_matrix

test_data = """
30373
25512
65332
33549
35390
"""

def test_map_visible():
    visible = np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
    ])
    trees = parse_digit_matrix(test_data)
    assert np.all(day_08.map_visible_trees(trees) == visible)
