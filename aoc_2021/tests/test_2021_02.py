from aoc_2021.day_02 import parse_instr, track_sub

EXAMPLE = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


def test_parse_instr():
    assert parse_instr(EXAMPLE.splitlines()) == [
        ("forward", 5),
        ("down", 5),
        ("forward", 8),
        ("up", 3),
        ("down", 8),
        ("forward", 2),
    ]


def test_track_sub():
    moves = parse_instr(EXAMPLE.splitlines())
    assert track_sub(moves) == (15, 60, 10)
