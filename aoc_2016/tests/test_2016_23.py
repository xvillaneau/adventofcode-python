from aoc_2016.day_23 import *

EXAMPLE = """
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
""".lstrip()


def test_run_program():
    program = parse_program(EXAMPLE)
    registers = run_program(program)
    assert registers[0] == 3
