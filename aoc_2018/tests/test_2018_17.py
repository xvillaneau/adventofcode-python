from aoc_2018.day_17 import *

EXAMPLE = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""".lstrip()


def test_parse_input():
    segments = parse_input(EXAMPLE)
    assert len(segments) == 8


def test_run_flows():
    matrix, start = build_matrix(EXAMPLE)
    run_flows(matrix, start)
    assert np.sum(matrix == WATER) == 29
    assert np.sum(matrix == STREAM) == 28
    assert np.sum(matrix & 1) == 57
