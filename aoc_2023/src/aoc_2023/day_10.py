from collections.abc import Iterator
from functools import lru_cache
from typing import Optional

import numpy as np

from libaoc.vectors import Vect2D, UP, DOWN, LEFT, RIGHT

SEGMENTS: dict[str, frozenset[Vect2D]] = {
    "|": frozenset([UP, DOWN]),
    "-": frozenset([LEFT, RIGHT]),
    "L": frozenset([UP, RIGHT]),
    "F": frozenset([RIGHT, DOWN]),
    "7": frozenset([DOWN, LEFT]),
    "J": frozenset([LEFT, UP]),
}


def load_grid(data: str):
    from libaoc.matrix import load_string_matrix

    return np.rot90(load_string_matrix(data), 3)


def setup_start(grid) -> Vect2D:
    """
    Finds the start of the pipe loop, and replaces its symbol with the
    pipe segment needed to connect it to the loop.
    """
    args = np.argwhere(grid == 'S')
    assert args.shape == (1, 2)
    start = Vect2D(*args[0])

    links = set()
    for d in (UP, DOWN, LEFT, RIGHT):
        pipe = grid[*(start+d)]
        if pipe == ".":
            continue
        if -d in SEGMENTS[pipe]:
            links.add(d)
        if len(links) == 2:
            break
    start_pipe = next(p for p, d in SEGMENTS.items() if d == links)
    grid[*start] = start_pipe

    return start


def next_direction(grid, pos: Vect2D, in_dir: Vect2D) -> Vect2D:
    out_dir = _next_dir(grid[*pos], in_dir)
    if out_dir is None:
        raise ValueError
    return out_dir


@lru_cache(maxsize=None)
def _next_dir(pipe: str, d: Vect2D) -> Optional[Vect2D]:
    if pipe == ".":
        return None
    dirs = SEGMENTS[pipe] - {-d}
    if len(dirs) != 1:
        return None
    out, = dirs
    return out


def follow_loop(grid, start: Vect2D) -> Iterator[tuple[Vect2D, Vect2D]]:
    next_dir, prev_dir = SEGMENTS[grid[*start]]
    yield start, next_dir - prev_dir  # First prev_dir is reversed

    pos = start + next_dir
    while pos != start:
        prev_dir = next_dir
        next_dir = next_direction(grid, pos, next_dir)
        yield pos, next_dir + prev_dir

        pos = pos + next_dir


def main(data: str):
    grid = load_grid(data)
    start = setup_start(grid)

    # Let's solve this using the magic of topology!
    # General idea: assume we have a closed line delimiting an area.
    # If move and keep track of how many times we cross a closed line,
    # then any time that count is ODD we are INSIDE the area.

    # We iterate over positions on the loop AND the move vectors,
    # and keep a map of the vertical component of those vectors.
    v_topo = np.zeros(grid.shape, dtype="int8")
    loop_tiles = np.zeros(grid.shape, dtype=bool)

    length = 0
    for pos, d in follow_loop(grid, start):
        v_topo[*pos] = d.y
        loop_tiles[*pos] = True
        length += 1
    yield length

    # Accumulate the vertical components along the horizontal axis.
    # Examples: (path --> v_topo --> topo)
    #  . F - 7 . --> 0  1  0 -1  0 --> 0 1 1 0 0
    #  . F - J . --> 0  1  0  1  0 --> 0 1 1 2 2
    # Because a single tile counts for two units of movement,
    # the areas inside the loop will have a counts of 4*n + 2.
    # Removing the loop tiles reveals the enclosed areas only.
    topo = np.cumsum(v_topo, axis=0) % 4
    yield np.count_nonzero(np.where(loop_tiles, 0, topo))
