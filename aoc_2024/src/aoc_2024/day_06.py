from typing import Iterator

import numpy as np

from libaoc.matrix import load_string_matrix
from libaoc.vectors import Direction, StaticWalker, Vect2D


class LoopDetected(Exception):
    pass


def parse_input(data: str) -> tuple[np.array, Vect2D]:
    lab = load_string_matrix(data)
    walls = lab == "#"

    pos = np.argwhere(lab == "^")
    assert pos.shape == (1, 2)
    start = Vect2D(int(pos[0, 0]), int(pos[0, 1]))

    return walls, start


def run_guard(lab, guard: StaticWalker, visited: set[StaticWalker] = None) -> Iterator[StaticWalker]:
    mx, my = lab.shape
    if visited is None:
        visited: set[StaticWalker] = set()
    visited.add(guard)

    while True:
        yield guard
        visited.add(guard)

        nxt = guard.move()
        p = nxt.pos
        if not (0 <= p.x < mx and 0 <= p.y < my):
            return

        if lab[p.x, p.y] > 0:  # Wall
            guard = guard.rot_right()
        else:
            guard = nxt

        if guard in visited:
            raise LoopDetected


def main(data: str):
    lab, start = parse_input(data)
    mx, my = lab.shape

    guard = StaticWalker(start, Direction.Left)

    visited: set[Vect2D] = set()
    path: set[StaticWalker] = set()
    obstructions: set[Vect2D] = set()

    for state in run_guard(lab, guard):
        visited.add(state.pos)
        path.add(state)

        p = state.move().pos
        if not (0 <= p.x < mx and 0 <= p.y < my):
            break
        if lab[p.x, p.y] > 0:
            continue  # No alt needed
        if p in visited:
            continue

        alt_lab = np.copy(lab)
        alt_lab[p.x, p.y] = True

        try:
            for _ in run_guard(alt_lab, state, path.copy()):
                pass
        except LoopDetected:
            obstructions.add(p)

    yield len(visited)
    yield len(obstructions)
