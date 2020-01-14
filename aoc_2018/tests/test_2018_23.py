from aoc_2018.day_23 import *

EXAMPLE = """
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
""".lstrip()


def test_range_of_largest():
    nanobots = parse_input(EXAMPLE)
    assert range_of_strongest(nanobots) == 7
