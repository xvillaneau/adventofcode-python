
from typing import List

from libaoc import simple_main, files
from libaoc.vectors import Walker2D, Direction, Instruction


def read_instructions(year, day):
    raw_data = files.read_full(year, day)
    elems = raw_data.split(', ')
    out = []

    for elem in elems:
        out.append(Instruction(elem[0]))
        moves = int(elem[1:])
        out.extend([Instruction.Move] * moves)

    return out


def walk_full(instructions: List[Instruction]):
    walker = Walker2D(0, 0, Direction.Up)
    for instruction in instructions:
        walker.do(instruction)
    return calc_dist(walker)


def walk_first_visited(instructions: List[Instruction]):
    walker = Walker2D(0, 0, Direction.Up)
    visited = {walker.pos}

    for instruction in instructions:
        walker.do(instruction)
        if instruction == Instruction.Move and walker.pos in visited:
            break
        visited.add(walker.pos)

    return calc_dist(walker)


def calc_dist(walker: Walker2D):
    return sum(walker.pos)


if __name__ == '__main__':
    simple_main(2016, 1, read_instructions, walk_full, walk_first_visited)
