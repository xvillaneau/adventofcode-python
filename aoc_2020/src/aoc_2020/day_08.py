from functools import reduce
from enum import Enum
from typing import List, Tuple


class Instr(str, Enum):
    NoOp = "nop"
    Incr = "acc"
    Jump = "jmp"


Program = List[Tuple[Instr, int]]


def parse_program(data: List[str]) -> Program:
    def parse_instr(line: str):
        instr, _, val = line.partition(" ")
        return Instr(instr), int(val)
    return list(map(parse_instr, data))


def run_program(program: Program):
    """
    Iterate over the instructions of the program until it terminates or
    starts looping.  Yields the accumulator value and program pointer
    value *BEFORE* each step.  If it terminates, yields an extra result
    with the final value of the accumulator.
    """
    acc, ptr, end = 0, 0, len(program)
    visited = [False] * len(program)

    while ptr < end and not visited[ptr]:
        yield (acc, ptr)
        visited[ptr] = True

        instr, val = program[ptr]
        if instr is Instr.Incr:
            acc += val
            ptr += 1
        elif instr is Instr.Jump:
            ptr += val
        else:
            ptr += 1

    yield acc, ptr


def final_accumulator(program: Program) -> int:
    """
    Get the final accumulator value either after the program terminates
    or before it starts looping infinitely.
    """
    return reduce(lambda _, y: y[0], run_program(program), 0)


def find_corrupt(program: Program) -> int:
    """
    Detect the address of a single instruction that can be modified to
    make the program terminate.  Returns a negative value if the program
    already terminates or cannot be modified.
    """

    # First, build a reversed graph of the program's sequence
    jumps_to = [[] for _ in range(len(program) + 1)]
    for ptr, (instr, val) in enumerate(program):
        dest = ptr + (val if instr is Instr.Jump else 1)
        jumps_to[dest].append(ptr)

    # Traverse that graph from the end to map all instructions that
    # eventually lead to the program terminating
    terminates = [False] * (len(program) + 1)
    frontier = [len(program)]
    while frontier:
        pos = frontier.pop()
        if terminates[pos]:
            continue
        terminates[pos] = True
        frontier.extend(jumps_to[pos])

    if terminates[0]:
        # Nothing to do
        return -1

    # Finally, go through the program from the beginning, and for every
    # jmp or nop check if the next address obtained by switching the
    # instruction can terminate.
    for _, ptr in run_program(program):
        instr, val = program[ptr]
        if instr is Instr.Incr:
            continue
        switch_dest = ptr + (1 if instr is Instr.Jump else val)
        if terminates[switch_dest]:
            return ptr

    return -2


def fix_program(program: Program) -> Program:
    """
    Analyze the program and modify a single instruction (nop <-> jmp) so
    that it does not loop forever.  If that change is possible, a copy
    of the program is created and the one passed is left unchanged.
    """
    if (pos := find_corrupt(program)) == -2:
        raise ValueError("Program cannot be fixed to terminate")
    elif pos == -1:
        return program

    program = program.copy()
    instr, val = program[pos]
    if instr is Instr.Incr:
        raise ValueError("Can only repair nop or jmp")
    instr = Instr.Jump if instr is Instr.NoOp else Instr.NoOp
    program[pos] = (instr, val)
    return program


def main(data: str):
    program = parse_program(data.splitlines())
    yield final_accumulator(program)
    fixed_program = fix_program(program)
    yield final_accumulator(fixed_program)
