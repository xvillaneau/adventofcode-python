from dataclasses import dataclass
from itertools import count, islice
from typing import Callable, List

from .day_12 import PARSERS, value_getter, parse_code


@dataclass
class OutSignal:
    getter: Callable[[List[int]], int]


def parse_out(x):
    return OutSignal(value_getter(x))


PARSERS["out"] = parse_out


def run_antenna(program, value):
    registers = [value, 0, 0, 0]
    pointer = 0
    while 0 <= pointer < len(program):
        op = program[pointer]
        if isinstance(op, OutSignal):
            yield op.getter(registers)
            res = None
        else:
            res = op(registers)
        pointer += 1 if not res else res


def main(data: str):
    program = parse_code(data)
    pattern = [0, 1] * 10
    for value in count():
        sample = list(islice(run_antenna(program, value), 20))
        if sample == pattern:
            yield value
            return
