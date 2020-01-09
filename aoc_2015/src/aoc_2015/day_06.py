import re
from typing import List, Tuple

import numpy as np


TURN_ON, TURN_OFF, TOGGLE = 0, 1, 2
Instruction = Tuple[int, slice, slice]
RE_INSTRUCTION = re.compile(r"(.*) (\d+),(\d+) through (\d+),(\d+)")


def parse_instructions(data: str) -> List[Instruction]:
    instructions = []
    for line in data.splitlines():
        op, x1, y1, x2, y2 = RE_INSTRUCTION.fullmatch(line).groups()
        if op == "turn on":
            action = TURN_ON
        elif op == "turn off":
            action = TURN_OFF
        elif op == "toggle":
            action = TOGGLE
        else:
            raise ValueError(f"Invalid input: {line}")
        slice_x = slice(int(x1), int(x2) + 1)
        slice_y = slice(int(y1), int(y2) + 1)
        instructions.append((action, slice_x, slice_y))
    return instructions


def run_simple_lamps(instructions: List[Instruction], dim=(1000, 1000)):
    lamps = np.zeros(dim, dtype=bool)
    for action, slice_x, slice_y in instructions:
        if action == TURN_ON:
            lamps[slice_x, slice_y] = True
        elif action == TURN_OFF:
            lamps[slice_x, slice_y] = False
        else:  # Toggle
            lamps[slice_x, slice_y] ^= True
    return np.sum(lamps)


def run_controllable_lamps(instructions: List[Instruction], dim=(1000, 1000)):
    lamps = np.zeros(dim, dtype=int)
    for action, slice_x, slice_y in instructions:
        if action == TURN_ON:
            lamps[slice_x, slice_y] += 1
        elif action == TURN_OFF:
            lamps[slice_x, slice_y] = np.maximum(lamps[slice_x, slice_y] - 1, 0)
        else:  # Toggle
            lamps[slice_x, slice_y] += 2
    return np.sum(lamps)


def main(data: str):
    instructions = parse_instructions(data)
    yield run_simple_lamps(instructions)
    yield run_controllable_lamps(instructions)
