from aoc_2023 import day_09

EXAMPLE = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""".strip()


def test_extrapolate():
    assert day_09.extrapolate([0, 3, 6, 9, 12, 15]) == (-3, 18)
    assert day_09.extrapolate([1, 3, 6, 10, 15, 21]) == (0, 28)
    assert day_09.extrapolate([10, 13, 16, 21, 30, 45]) == (5, 68)
