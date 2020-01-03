"""
Advent of Code 2019 day 3, simple solution
https://adventofcode.com/2019/day/3

Run it with:  python run_aoc.py 2019 3 simple
Read the docs at:  /aoc_2019/docs/day_03.md
"""


def segment_path(start, direction, moves):
    """Get the coordinates of all points on a segment"""
    x0, y0 = start
    if direction == "U":  # Increase Y
        return [(x0, y0 + y) for y in range(1, moves + 1)]
    elif direction == "D":  # Decrease Y
        return [(x0, y0 - y) for y in range(1, moves + 1)]
    elif direction == "R":  # Increase X
        return [(x0 + x, y0) for x in range(1, moves + 1)]
    else:  # Going left, decrease X
        return [(x0 - x, y0) for x in range(1, moves + 1)]


def compute_path(wire):
    """Get all the positions occupied by a wire, with a count of steps"""
    path, steps, start = {}, 1, (0, 0)

    for direction, moves in wire:
        for point in segment_path(start, direction, moves):
            path.setdefault(point, steps)
            start = point
            steps += 1

    return path


def parse_wire(data):
    """Convert a line of input data into segment tuples"""
    return [(word[0], int(word[1:])) for word in data.split(",")]


def main(data):
    # Input data has one wire per line
    raw_1, raw_2 = data.strip().splitlines()
    path_1 = compute_path(parse_wire(raw_1))
    path_2 = compute_path(parse_wire(raw_2))
    intersections = path_1.keys() & path_2.keys()

    yield min(abs(x) + abs(y) for x, y in intersections)
    yield min(path_1[pt] + path_2[pt] for pt in intersections)


if __name__ == "__main__":
    import sys

    with open(sys.argv[1]) as file:
        _main = main(file.read())
    print(f"Aoc 2019, day 3, part 1:", next(_main))
    print(f"Aoc 2019, day 3, part 2:", next(_main))
