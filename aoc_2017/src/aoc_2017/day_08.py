from collections import defaultdict
import re
from typing import Tuple, List, Dict

Instruction = Tuple[str, str]

CONDITIONS = {
    ">": int.__gt__, ">=": int.__ge__,
    "<": int.__lt__, "<=": int.__le__,
    "==": int.__eq__, "!=": int.__ne__}

OPERATIONS = {'inc': int.__add__, 'dec': int.__sub__}


def parse_line(line: str) -> Instruction:
    return re.match(r"^([a-z]+ .*) if (.*)$", line).groups()


def parse_file(lines: List[str]) -> List[Instruction]:
    return [parse_line(line) for line in lines if line]


def apply_condition(registers: Dict[str, int], condition: str) -> bool:
    reg, test, val = condition.split()
    return CONDITIONS[test](registers[reg], int(val))


def apply_operation(registers: Dict[str, int], instruction: str):
    reg, oper, val = instruction.split()
    registers[reg] = OPERATIONS[oper](registers[reg], int(val))


def run_program(program: List[str]) -> Tuple[int, int]:
    instructions = parse_file(program)

    registers = defaultdict(int)
    highest = 0

    for operation, condition in instructions:
        if apply_condition(registers, condition):
            apply_operation(registers, operation)
            reg = operation.split()[0]
            highest = max(highest, registers[reg])

    return max(registers.values()), highest


if __name__ == '__main__':
    from libaoc import tuple_main, files
    tuple_main(2017, 8, files.read_lines, run_program)
