from aoc_2021.day_17 import count_trajectories, parse_target


def test_parse_target():
    example = "target area: x=20..30, y=-10..-5"
    assert parse_target(example) == (20, 30, -10, -5)

def test_count_trajectories():
    assert count_trajectories(20, 30, -10, -5) == 112
