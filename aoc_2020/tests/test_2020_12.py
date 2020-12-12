from aoc_2020.day_12 import move_ship, move_with_waypoint

EXAMPLE = """
F10
N3
F7
R90
F11
""".strip().splitlines()


def test_move_ship():
    assert move_ship(EXAMPLE) == (17, -8)


def test_move_with_waypoint():
    assert move_with_waypoint(EXAMPLE) == (214, -72)
