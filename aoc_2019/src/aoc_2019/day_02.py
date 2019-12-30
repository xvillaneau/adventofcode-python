"""
Advent of Code 2019, day 2
https://adventofcode.com/2019/day/2

For a longer explanation of the problem and my solution, read:
https://github.com/xvillaneau/adventofcode-python/wiki/AoC-2019-Day-2
"""
from typing import List

from libaoc import BaseRunner
from .intcode import CodeRunner


def input_and_run(code: List[int], noun=12, verb=2):
    """
    Set the correct values in memory, run the code and get the output
    (value at address 0 in memory) back.
    """
    runner = CodeRunner(code)
    runner.code[1], runner.code[2] = noun, verb
    runner.run_full()
    return runner.code[0]


def find_input(code: List[int], target=19_690_720):
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


class AocRunner(BaseRunner):
    year = 2019
    day = 2
    parser = BaseRunner.int_list_parser(",")

    def run(self, data: List[int]):
        yield input_and_run(data)
        yield find_input(data)
