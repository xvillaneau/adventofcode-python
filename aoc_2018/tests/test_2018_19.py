from aoc_2018.day_19 import *

EXAMPLE = """
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
""".strip()


def test_parse_input():
    addi, addr, seti, setr = (
        OPERATIONS[name] for name in ("addi", "addr", "seti", "setr")
    )
    pointer, program = parse_input(EXAMPLE)
    assert pointer == 0
    assert program == [
        (seti, 5, 0, 1),
        (seti, 6, 0, 2),
        (addi, 0, 1, 0),
        (addr, 1, 2, 3),
        (setr, 1, 0, 0),
        (seti, 8, 0, 4),
        (seti, 9, 0, 5),
    ]


def test_run():
    registers = run_program(*parse_input(EXAMPLE))
    assert registers == [6, 5, 6, 0, 0, 9]
