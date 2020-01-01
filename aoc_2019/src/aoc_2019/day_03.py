"""
Advent of Code 2019 day 3
https://adventofcode.com/2019/day/3

Run it with:  python run_aoc.py 2019 3
Read the docs at:  /aoc_2019/docs/day_03.md
"""
from dataclasses import dataclass
from functools import cached_property
from itertools import product
from typing import Iterator, Dict, List, Tuple

Point = Tuple[int, int]


DIRECTIONS = {"U": (0, 1), "R": (1, 0), "D": (0, -1), "L": (-1, 0)}


@dataclass(frozen=True)
class Segment:
    start: Point
    direction: str
    moves: int
    index: int

    @cached_property
    def end(self) -> Point:
        (x, y), (dx, dy) = self.start, DIRECTIONS[self.direction]
        return x + self.moves * dx, y + self.moves * dy

    @cached_property
    def span(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        (x, y), (dx, dy) = self.start, DIRECTIONS[self.direction]
        x0, x1 = sorted([x + dx, self.end[0]])
        y0, y1 = sorted([y + dy, self.end[1]])
        return (x0, x1), (y0, y1)

    @cached_property
    def trace(self) -> Dict[Point, int]:
        return {point: steps for steps, point in self}

    def overlaps(self, other: 'Segment') -> bool:
        (ax, ay), (bx, by) = self.span, other.span
        return ax[0] <= bx[1] and ax[1] >= bx[0] and ay[0] <= by[1] and ay[1] >= by[0]

    def __iter__(self):
        x0, y0 = self.start
        indices = range(1, self.moves + 1)
        if self.direction == "U":
            coords = ((x0, y0 + y) for y in indices)
        elif self.direction == "D":
            coords = ((x0, y0 - y) for y in indices)
        elif self.direction == "R":
            coords = ((x0 + x, y0) for x in indices)
        else:
            coords = ((x0 - x, y0) for x in indices)
        yield from enumerate(coords, start=self.index + 1)

    def __and__(self, other: 'Segment') -> List[Tuple[Point, int, int]]:
        if not self.overlaps(other):
            return []
        intersections = self.trace.keys() & other.trace.keys()
        return [(pt, self.trace[pt], other.trace[pt]) for pt in intersections]


Path = Iterator[Segment]


def parse_input(data: str) -> Tuple[Path, Path]:

    def generate_path(path: str):
        moves, pos = 0, (0, 0)
        for word in path.split(","):
            segment = Segment(pos, word[0], int(word[1:]), moves)
            yield segment
            pos = segment.end
            moves += segment.moves

    path_1, path_2 = data.strip().splitlines()
    return generate_path(path_1), generate_path(path_2)


def main(data: str):
    path_1, path_2 = parse_input(data)
    intersections = {}

    for seg_a, seg_b in product(path_1, path_2):
        for point, ind_a, ind_b in seg_a & seg_b:
            intersections[point] = (ind_a, ind_b)

    yield min(abs(x) + abs(y) for x, y in intersections)
    yield min(a + b for a, b in intersections.values())
