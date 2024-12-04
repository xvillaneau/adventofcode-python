import pytest

from aoc_2023 import day_08

EXAMPLE_1 = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
EXAMPLE_2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


def test_parse_data():
    directions, nodes = day_08.parse_data(EXAMPLE_1)
    assert directions == "RL"
    assert len(nodes) == 7
    assert nodes["AAA"] == ("BBB", "CCC")


@pytest.mark.parametrize("data,steps", [(EXAMPLE_1, 2), (EXAMPLE_2, 6)])
def test_part_1(data, steps):
    directions, nodes = day_08.parse_data(data)
    assert day_08.count_steps(directions, nodes) == steps
