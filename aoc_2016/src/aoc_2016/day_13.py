from collections import deque
from functools import lru_cache, partial
from math import dist
from typing import NamedTuple

from libaoc.algo import AStarSearch


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Pos"):
        return Pos(self.x + other.x, self.y + other.y)


@lru_cache(maxsize=512)
def is_wall(pos: Pos, offset: int) -> bool:
    x, y = pos
    if x < 0 or y < 0:
        return True
    _sum = x * x + 3 * x + 2 * x * y + y + y * y + offset
    bits = 0
    while _sum:
        bits += _sum & 1
        _sum >>= 1
    return bool(bits & 1)


MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def successors(offset: int, pos: Pos):
    result = []
    for x, y in MOVES:
        next_pos = Pos(pos.x + x, pos.y + y)
        if not is_wall(next_pos, offset):
            result.append(next_pos)
    return result


def shortest_path(offset: int, end: Pos = Pos(31, 39), start: Pos = Pos(1, 1)):
    searcher = AStarSearch(
        start, end.__eq__, partial(successors, offset), partial(dist, end)
    )
    result = searcher.search()
    if result is None:
        raise RuntimeError
    return len(result.path()) - 1


def count_reachable(offset: int, depth=50, start=Pos(1, 1)):
    frontier = deque([(start, 0)])
    explored = {start: 0}

    while frontier:
        current_pos, current_depth = frontier.popleft()

        if current_depth >= depth:
            continue

        for child in successors(offset, current_pos):
            new_depth = current_depth + 1
            if child in explored and explored[child] <= new_depth:
                continue
            explored[child] = new_depth
            frontier.append((child, new_depth))

    return len(explored)


def main(data: str):
    offset = int(data)
    yield shortest_path(offset)
    yield count_reachable(offset)
