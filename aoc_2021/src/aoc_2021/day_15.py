import numpy as np

from libaoc.algo import CostAStarSearch
from libaoc.parsers import parse_digit_matrix


def low_risk_path(cave_map: np.ndarray):
    max_x, max_y = cave_map.shape
    goal = (max_x - 1, max_y - 1)

    def successors(pos: tuple[int, int]):
        x, y = pos
        neighbors = []

        def add_point(u, v):
            if 0 <= u < max_x and 0 <= v < max_y:
                neighbors.append(((u, v), cave_map[u, v]))

        add_point(x - 1, y)
        add_point(x + 1, y)
        add_point(x, y - 1)
        add_point(x, y + 1)
        return neighbors

    search: CostAStarSearch[tuple[int, int]] = CostAStarSearch(
        (0, 0), (lambda p: p == goal), successors
    )
    return int(search.search().cost)


def low_risk_path_5x(cave_map: np.ndarray):
    bx, by = cave_map.shape
    goal = (bx * 5 - 1, by * 5 - 1)

    def successors(pos: tuple[int, int]):
        x, y = pos
        neighbors = []

        def add_point(u, v):
            if 0 <= u < 5 * bx and 0 <= v < 5 * by:
                nu, ru = divmod(u, bx)
                nv, rv = divmod(v, by)
                cost = 1 + (cave_map[ru, rv] + nu + nv - 1) % 9
                neighbors.append(((u, v), cost))

        add_point(x - 1, y)
        add_point(x + 1, y)
        add_point(x, y - 1)
        add_point(x, y + 1)
        return neighbors

    search: CostAStarSearch[tuple[int, int]] = CostAStarSearch(
        (0, 0), (lambda p: p == goal), successors
    )
    return int(search.search().cost)


def main(data: str):
    caves = parse_digit_matrix(data)
    yield low_risk_path(caves)
    yield low_risk_path_5x(caves)
