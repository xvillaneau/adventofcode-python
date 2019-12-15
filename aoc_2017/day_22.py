from itertools import islice
from typing import Generator, List, Set, Tuple


Node = Tuple[int, int]
Grid = Set[Node]
StrongGrid = Tuple[Grid, Grid, Grid]  # Weak, Infected, Flagged
Vector = Tuple[int, int]

UP = (0, 1)
RIGHT = (1, 0)
DOWN = (0, -1)
LEFT = (-1, 0)
DIRS = [UP, RIGHT, DOWN, LEFT]


def read_map(lines: List[str]) -> Grid:
    lines = [l for l in lines if l.strip()]
    n = len(lines)
    assert n % 2 == 1
    assert all(len(l) == n for l in lines)
    c = n // 2

    grid = set((j - c, c - i)
               for i, l in enumerate(lines)
               for j, p in enumerate(l)
               if p == '#')
    return grid


def turn_left(vector: Vector) -> Vector:
    left = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}
    return left[vector]


def turn_right(vector: Vector) -> Vector:
    right = {UP: RIGHT, LEFT: UP, DOWN: LEFT, RIGHT: DOWN}
    return right[vector]


def turn_back(vector: Vector) -> Vector:
    x, y = vector
    return -x, -y


def step_turn(grid: Grid, pos: Node, heading: Vector) -> Vector:
    f = turn_right if pos in grid else turn_left
    return f(heading)


def step_turn_strong(grid: StrongGrid, pos: Node, heading: Vector) -> Vector:
    weak, infect, flag = grid
    if pos in weak:
        return heading
    elif pos in infect:
        return turn_right(heading)
    elif pos in flag:
        return turn_back(heading)
    else:
        return turn_left(heading)


def step_toggle(grid: Grid, pos: Node) -> Grid:
    new_grid = grid.copy()
    if pos in new_grid:
        new_grid.remove(pos)
    else:
        new_grid.add(pos)
    return new_grid


def step_toggle_strong(grid: StrongGrid, pos: Node) -> None:
    weak, infect, flag = grid

    if pos in weak:
        infect.add(pos)
        weak.remove(pos)
    elif pos in infect:
        flag.add(pos)
        infect.remove(pos)
    elif pos in flag:
        flag.remove(pos)
    else:
        weak.add(pos)


def step_move(pos: Node, heading: Vector) -> Node:
    x, y = pos
    u, v = heading
    return x + u, y + v


def virus_burst(grid: Grid, pos: Node, heading: Vector) -> Tuple[Grid, Node, Vector, bool]:
    infected = pos not in grid
    heading = step_turn(grid, pos, heading)
    grid = step_toggle(grid, pos)
    pos = step_move(pos, heading)
    return grid, pos, heading, infected


def virus_burst_strong(grid: StrongGrid, pos: Node, heading: Vector) -> Tuple[Node, Vector, bool]:
    infected = pos in grid[0]
    new_heading = step_turn_strong(grid, pos, heading)
    step_toggle_strong(grid, pos)
    new_pos = step_move(pos, new_heading)
    return new_pos, new_heading, infected


def virus_gen(grid: Grid) -> Generator[Tuple[Grid, int], None, None]:
    pos, heading, count = (0, 0), UP, 0

    while True:
        grid, pos, heading, infected = virus_burst(grid, pos, heading)
        count += 1 if infected else 0
        yield grid, count


def virus_count(grid: Grid, bursts: int) -> int:
    virus = virus_gen(grid)
    _, count = next(islice(virus, bursts - 1, bursts))
    return count


def virus_count_strong(infected: Grid, bursts: int) -> int:

    pos, heading, count = (0, 0), UP, 0
    grid = (set([]), infected.copy(), set([]))

    for _ in range(bursts):
        pos, heading, infected = virus_burst_strong(grid, pos, heading)
        count += 1 if infected else 0

    return count


def day_22(lines: List[str]):
    grid = read_map(lines)
    yield virus_count(grid, 10_000)
    yield virus_count_strong(grid, 10_000_000)


if __name__ == '__main__':
    from libaoc import iter_main, files
    iter_main(2017, 22, files.read_lines, day_22)
