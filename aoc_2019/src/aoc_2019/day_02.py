"""
Advent of Code 2019, day 2
https://adventofcode.com/2019/day/2

Run it with:  python run_aoc.py 2019 2
Read the docs at:  /aoc_2019/docs/day_02.md
"""
from .intcode import CodeRunner, parse_intcode


def input_and_run(code, noun=12, verb=2):
    """
    Set the correct values in memory, run the code and get the output
    (value at address 0 in memory) back.
    """
    runner = CodeRunner(code)
    runner.code[1], runner.code[2] = noun, verb
    runner.run_full()
    return runner.code[0]


def find_input(code, target=19_690_720):
    """
    Assumption-heavy optimization: the code output is linear per the
    inputs, i.e. output = const + dn * noun + dv * verb
    That way we only need three points to find the address we want,
    instead of many thousands.
    """
    corner_00 = input_and_run(code, 0, 0)
    corner_10 = input_and_run(code, 99, 0)
    corner_01 = input_and_run(code, 0, 99)

    dn, rn = divmod(corner_10 - corner_00, 99)
    dv, rv = divmod(corner_01 - corner_00, 99)
    assert rn == rn == 0

    relative_target = target - corner_00
    noun, rn = divmod(relative_target, dn)
    verb, rv = divmod(rn, dv)
    assert 0 <= noun < 100
    assert 0 <= verb < 100
    assert rv == 0

    return 100 * noun + verb


def main(data: str):
    code = parse_intcode(data)
    yield input_and_run(code)
    yield find_input(code)
