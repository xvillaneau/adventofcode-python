from aoc_2018.day_22 import *

EXAMPLE = """
depth: 510
target: 10,10
""".lstrip()


def test_risk_score():
    depth, target = parse_input(EXAMPLE)
    assert risk_score(build_map(depth, target), target) == 114


def test_shortest_hike():
    depth, target = parse_input(EXAMPLE)
    levels = build_map(depth, target)
    assert shortest_hike(levels, depth, target) == 45
