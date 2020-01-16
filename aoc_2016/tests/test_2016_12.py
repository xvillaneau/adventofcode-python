from aoc_2016.day_12 import *

EXAMPLE = """
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
""".lstrip()


def test_run_code():
    program = parse_code(EXAMPLE)
    registers = run_code(program)
    assert registers[0] == 42
