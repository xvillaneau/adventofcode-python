import pytest

from aoc_2022 import day_13

EXAMPLE = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

def test_parse_input():
    pairs = day_13.parse_input(EXAMPLE)
    assert len(pairs) == 8
    assert all(len(p) == 2 for p in pairs)


@pytest.mark.parametrize("packet,expected", [
    (ln, eval(ln)) for ln in EXAMPLE.strip().splitlines() if ln
])
def test_parse_packet(packet, expected):
    assert day_13.parse_packet(packet) == expected


EXAMPLE_RES = [True, True, False, True, False, True, False, False]

@pytest.mark.parametrize("pair,in_order", zip(day_13.parse_input(EXAMPLE), EXAMPLE_RES))
def test_compare(pair, in_order):
    res = day_13.compare(*pair)
    if in_order:
        assert res < 0
    else:
        assert res > 0


def test_part_1():
    pairs = day_13.parse_input(EXAMPLE)
    assert day_13.part_1(pairs) == 13


def test_part_2():
    pairs = day_13.parse_input(EXAMPLE)
    assert day_13.part_2(pairs) == 140
