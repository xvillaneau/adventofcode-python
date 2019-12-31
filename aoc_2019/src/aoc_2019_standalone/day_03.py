def span_direction(start, direction, moves):
    x0, y0 = start
    if direction in "UD":
        dy = 1 if direction == "U" else -1
        for y in range(dy, (moves + 1) * dy, dy):
            yield x0, y0 + y
    else:
        dx = 1 if direction == "R" else -1
        for x in range(dx, (moves + 1) * dx, dx):
            yield x0 + x, y0


def trace(path):
    visited = {}
    steps = 1
    start = (0, 0)

    for direction, moves in path:
        for point in span_direction(start, direction, moves):
            if point not in visited:
                visited[point] = steps
            start = point
            steps += 1

    return visited


def parse_input(data):
    def split_path(_path: str):
        return ((word[0], int(word[1:])) for word in _path.split(","))

    path_1, path_2 = data.strip().splitlines()
    return split_path(path_1), split_path(path_2)


def main(data):
    path_1, path_2 = parse_input(data)
    trace_1, trace_2 = trace(path_1), trace(path_2)
    intersections = trace_1.keys() & trace_2.keys()

    yield min(abs(x) + abs(y) for x, y in intersections)
    yield min(trace_1[pt] + trace_2[pt] for pt in intersections)


if __name__ == "__main__":
    import sys

    with open(sys.argv[1]) as file:
        _main = main(file.read())
    print(f"Aoc 2019, day 3, part 1:", next(_main))
    print(f"Aoc 2019, day 3, part 2:", next(_main))
