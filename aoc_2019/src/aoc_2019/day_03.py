from typing import NamedTuple, Iterator, Dict, Tuple

from libaoc import BaseRunner
from libaoc.vectors import Vect2D

Path = Iterator[Tuple[str, int]]
Point = Tuple[int, int]


class Segment(NamedTuple):
    start: Vect2D
    direction: Vect2D
    moves: int
    start_steps: int


def span_direction(start: Point, direction: str, moves: int):
    x0, y0 = start
    if direction in "UD":
        dy = 1 if direction == "U" else -1
        y0 += dy
        for y in range(0, moves * dy, dy):
            yield x0, y0 + y
    else:
        dx = 1 if direction == "R" else -1
        x0 += dx
        for x in range(0, moves * dx, dx):
            yield x0 + x, y0


def trace(path: Path) -> Dict[Point, int]:
    visited, point, steps = {}, (0, 0), 1
    for direction, moves in path:
        for point in span_direction(point, direction, moves):
            visited.setdefault(point, steps)
            steps += 1
    return visited


def parse_input(_, data: str) -> Tuple[Path, Path]:
    def split_path(_path: str):
        return ((word[0], int(word[1:])) for word in _path.split(","))
    path_1, path_2 = data.strip().splitlines()
    return split_path(path_1), split_path(path_2)


class AocRunner(BaseRunner):
    year = 2019
    day = 3
    parser = parse_input

    def run(self, paths: Tuple[Path, Path]):
        path_1, path_2 = paths
        trace_1, trace_2 = trace(path_1), trace(path_2)
        intersections = trace_1.keys() & trace_2.keys()

        yield min(abs(x) + abs(y) for x, y in intersections)
        yield min(trace_1[pt] + trace_2[pt] for pt in intersections)
