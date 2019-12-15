from collections import defaultdict
from itertools import islice
from typing import Iterator, Iterable

from libaoc.vectors import Vect2D


def follow_instructions(instructions: Iterable[str]) -> Iterator[Vect2D]:
    pos = Vect2D(0, 0)
    moves = {'^': Vect2D.up, 'v': Vect2D.down, '>': Vect2D.right, '<': Vect2D.left}
    yield pos
    for instr in instructions:
        pos = moves[instr](pos)
        yield pos

def house_visits(instructions: Iterable[str]):
    houses = defaultdict(int)
    for pos in follow_instructions(instructions):
        houses[pos] += 1
    return houses

def count_one_visit(instructions: str):
    return len(house_visits(instructions.strip()))

def count_robosanta_visits(instructions: str):
    santa = house_visits(islice(instructions.strip(), 0, None, 2))
    robot = house_visits(islice(instructions.strip(), 1, None, 2))
    return len(santa.keys() | robot.keys())

def test_count_visits():
    assert count_one_visit('>') == 2
    assert count_one_visit('^>v<') == 4
    assert count_one_visit('^v^v^v^v^v') == 2

    assert count_robosanta_visits('^v') == 3
    assert count_robosanta_visits('^>v<') == 3
    assert count_robosanta_visits('^v^v^v^v^v') == 11

if __name__ == '__main__':
    from libaoc import simple_main, files
    simple_main(2015, 3, files.read_full, count_one_visit, count_robosanta_visits)
