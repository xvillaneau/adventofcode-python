from aoc_2016.day_24 import *

EXAMPLE = """
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
""".lstrip()


def test_shortest_visit():
    space, points = parse_map(EXAMPLE)
    assert shortest_visit(space, points) == 14
