from aoc_2015.day_06 import parse_instructions, run_simple_lamps, run_controllable_lamps

EXAMPLE = """
turn on 0,0 through 2,2
turn off 1,1 through 3,3
toggle 0,1 through 2,3
"""


def test_simple_lamps():
    instructions = parse_instructions(EXAMPLE.lstrip())
    assert run_simple_lamps(instructions, (4, 4)) == 10


def test_controllable_lamps():
    instructions = parse_instructions(EXAMPLE.lstrip())
    assert run_controllable_lamps(instructions, (4, 4)) == 23
