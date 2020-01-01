from aoc_2015.day_18 import animate, animate_stuck

example = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""

def test_animate():
    assert animate(example, 4) == 4

def test_animate_stuck():
    assert animate_stuck(example, 5) == 17
