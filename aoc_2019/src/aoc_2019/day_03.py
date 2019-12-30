from typing import NamedTuple, List, Iterator, Dict
from more_itertools import seekable

from libaoc import BaseRunner


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __abs__(self):
        return abs(self.x) + abs(self.y)

DIRS = {
    "U": Point(0, 1),
    "R": Point(1, 0),
    "D": Point(0, -1),
    "L": Point(-1, 0),
}

def move(start: Point, instruction: str):
    direction = DIRS[instruction[0]]
    moves = int(instruction[1:])
    point = start
    yield from (point := point + direction for _ in range(moves))

def path(instructions: List[str]) -> Iterator[Point]:
    point = Point(0, 0)
    for instruction in instructions:
        moves = seekable(move(point, instruction))
        yield from moves
        point = moves.elements()[-1]

def steps(instructions: List[str]) -> Dict[Point, int]:
    res = {}
    for i, point in enumerate(path(instructions)):
        if point not in res:
            res[point] = i + 1
    return res

def intersections(wire_1: List[str], wire_2: List[str]):
    return set(path(wire_1)) & set(path(wire_2))


class AocRunner(BaseRunner):
    year = 2019
    day = 3
    parser = BaseRunner.lines_parser()

    def run(self, data):
        l1, l2 = data
        w1, w2 = l1.split(','), l2.split(',')
        yield min(map(abs, intersections(w1, w2)))

        steps1, steps2 = steps(w1), steps(w2)
        yield min(
            steps1[pt] + steps2[pt]
            for pt in steps1.keys() & steps2.keys()
        )
