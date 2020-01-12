from typing import List, Tuple

from libaoc.math import all_factors
from .day_16 import OPERATIONS, Operation

Instruction = Tuple[Operation, int, int, int]
Program = List[Instruction]


def parse_input(data: str) -> Tuple[int, Program]:
    pointer_addr, program = 0, []

    for line in data.splitlines():
        if line.startswith("#ip"):
            pointer_addr = int(line[4])
        else:
            op, a, b, c, *_ = line.split(maxsplit=4)
            program.append((OPERATIONS[op], int(a), int(b), int(c)))

    return pointer_addr, program


def run_program(pointer_addr: int, program: Program, ini_zero=0, interrupt=-1):
    pointer, max_p = 0, len(program)
    registers = [0] * 6
    registers[0] = ini_zero

    while 0 <= pointer < max_p:
        if pointer == interrupt:
            break
        registers[pointer_addr] = pointer
        op, a, b, c = program[pointer]
        op(a, b, c, registers)
        pointer = registers[pointer_addr] + 1

    return registers


def cheat_program(pointer_addr, program: Program, ini_zero=0):
    # Will NOT WORK with other inputs! (probably).
    # This is the result of reverse-engineering my input.
    registers = run_program(pointer_addr, program, ini_zero=ini_zero, interrupt=1)
    return sum(all_factors(registers[1]))


def main(data: str):
    pointer_addr, program = parse_input(data)
    yield cheat_program(pointer_addr, program)
    yield cheat_program(pointer_addr, program, 1)
