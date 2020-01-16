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
    operation, condition = re.match(r"^([a-z]+ .*) if (.*)$", line).groups()
    return operation, condition


def parse_file(lines: List[str]) -> List[Instruction]:
    return [parse_line(line) for line in lines if line]


def apply_condition(registers: Dict[str, int], condition: str) -> bool:
    reg, test, val = condition.split()
    return CONDITIONS[test](registers[reg], int(val))


def apply_operation(registers: Dict[str, int], instruction: str):
    reg, oper, val = instruction.split()
    registers[reg] = OPERATIONS[oper](registers[reg], int(val))


def main(data: str):
    instructions = parse_file(data.splitlines())

    registers = defaultdict(int)
    highest = 0

    for operation, condition in instructions:
        if apply_condition(registers, condition):
            apply_operation(registers, operation)
            reg = operation.split()[0]
            highest = max(highest, registers[reg])

    yield max(registers.values())
    yield highest
