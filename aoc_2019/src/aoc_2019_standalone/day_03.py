from typing import Iterator, Dict, Tuple

Path = Iterator[Tuple[str, int]]
Point = Tuple[int, int]


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
    visited = {}
    steps = 1
    point = (0, 0)

    for direction, moves in path:
        for point in span_direction(point, direction, moves):
            visited.setdefault(point, steps)
            steps += 1

    return visited


def parse_input(filename) -> Tuple[Path, Path]:
    def split_path(_path: str):
        return ((word[0], int(word[1:])) for word in _path.split(","))
    with open(filename) as file:
        path_1, path_2 = file.read().strip().splitlines()
    return split_path(path_1), split_path(path_2)


def main(filename):
    path_1, path_2 = parse_input(filename)
    trace_1, trace_2 = trace(path_1), trace(path_2)
    intersections = trace_1.keys() & trace_2.keys()

    part_1 = min(abs(x) + abs(y) for x, y in intersections)
    print("Day 3, part 1:", part_1)
    part_2 = min(trace_1[pt] + trace_2[pt] for pt in intersections)
    print("Day 3, part 2:", part_2)
