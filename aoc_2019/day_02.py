from itertools import product
from typing import List

from aoc_2019.intcode import read_program, CodeRunner

def input_and_run(intcode: List[int], noun=12, verb=2):
    runner = CodeRunner(intcode)
    runner.code[1], runner.code[2] = noun, verb
    runner.run_full()
    return runner.code[0]

def find_input(intcode: List[int], target=19690720):
    for noun, verb in product(range(100), range(100)):
        if input_and_run(intcode, noun, verb) == target:
            return noun, verb
    raise ValueError

def part_2(intcode):
    noun, verb = find_input(intcode)
    return 100 * noun + verb


if __name__ == '__main__':
    from libaoc import simple_main
    simple_main(2019, 2, read_program, input_and_run, part_2)
