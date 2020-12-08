from aoc_2020.day_08 import final_accumulator, find_corrupt, fix_program, parse_program

EXAMPLE = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""".strip().splitlines()


def test_find_loop():
    assert final_accumulator(parse_program(EXAMPLE)) == 5


def test_analyze_program():
    assert find_corrupt(parse_program(EXAMPLE)) == 7


def test_fix_program():
    program = fix_program(parse_program(EXAMPLE))
    assert final_accumulator(program) == 8
    assert fix_program(program) is program
