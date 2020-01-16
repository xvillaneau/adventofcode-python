from functools import partial
from hashlib import md5
from typing import List, NamedTuple

from libaoc.algo import BFSearch, HighestCostSearch
from libaoc.vectors import Vect2D, UP, DOWN, LEFT, RIGHT


class MazeState(NamedTuple):
    position: Vect2D
    path: str


INITIAL = MazeState(Vect2D(0, 3), "")
END = Vect2D(3, 0)


def open_paths(seed: str, path: str) -> str:
    head = md5((seed + path).encode()).hexdigest()[:4]
    return "".join(door for door, c in zip("UDLR", head) if c in "bcdef")


DIRS = {"U": UP, "D": DOWN, "L": LEFT, "R": RIGHT}


def next_states(seed: str, state: MazeState) -> List[MazeState]:
    res = []
    for open_door in open_paths(seed, state.path):
        pos = state.position + DIRS[open_door]
        if not (0 <= pos.x < 4 and 0 <= pos.y < 4):
            continue
        res.append(MazeState(pos, state.path + open_door))
    return res


def at_end(state: MazeState):
    return state.position == END


def navigate_maze(seed: str):
    solver = BFSearch(INITIAL, at_end, partial(next_states, seed))
    result = solver.search()
    if result is not None:
        return result.state.path
    raise RuntimeError("No solution found!")


def exhaust_maze(seed: str):
    solver = HighestCostSearch(INITIAL, at_end, partial(next_states, seed))
    result = solver.search()
    if result is not None:
        return round(result.cost)
    raise RuntimeError("No solution found!")


def main(data: str):
    yield navigate_maze(data)
    yield exhaust_maze(data)
