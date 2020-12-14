from aoc_2020.day_14 import run_program, run_program_v2

EXAMPLE = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""".strip().splitlines()

EXAMPLE_V2 = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""".strip().splitlines()


def test_run_program():
    assert run_program(EXAMPLE) == {7: 101, 8: 64}


def test_run_program_v2():
    assert run_program_v2(EXAMPLE_V2) == {
        16: 1, 17: 1, 18: 1, 19: 1, 24: 1, 25: 1, 26: 1, 27: 1,
        58: 100, 59: 100,
    }
