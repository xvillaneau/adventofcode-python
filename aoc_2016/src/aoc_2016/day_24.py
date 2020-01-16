from collections import deque
from itertools import permutations
from typing import List, Tuple

import numpy as np

from libaoc.graph import HWeightedGraph
from libaoc.matrix import load_string_matrix

Pos = Tuple[int, int]


def parse_map(data: str):
    mat = load_string_matrix(data)
    space = (mat != "#")
    points_map = np.where(space, mat, ".")
    points_coords = np.nonzero(points_map != ".")

    points = [(0, 0)] * (max(map(int, mat[points_coords])) + 1)
    for x, y in zip(*points_coords):
        points[int(mat[x, y])] = (x, y)
    return space, points


def build_graph(space, points: List[Pos]):
    graph = HWeightedGraph(points)

    def neighbors(position: Pos):
        x, y = position
        pts = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
        return [pt for pt in pts if space[pt]]

    points_complete = set()
    for start in points:

        to_find = set(points) - {start} - points_complete
        frontier = deque([(0, start)])
        visited = {start}

        while to_find and frontier:
            dist, pos = frontier.popleft()

            if pos in to_find:
                graph.add_edge(start, pos, dist)
                to_find.remove(pos)

            next_dist = dist + 1
            for next_pos in neighbors(pos):
                if next_pos in visited:
                    continue
                visited.add(next_pos)
                frontier.append((next_dist, next_pos))

        points_complete.add(start)

    return graph


def shortest_visit(space, points: List[Pos]):
    graph = build_graph(space, points)
    start = points[0]
    points = points[1:]

    def visit_length(order: List[Pos]):
        prev = start
        length = 0
        for point in order:
            length += next(n for v, n in graph.neighbors_of(prev) if v == point)
            prev = point
        return length

    return min(visit_length(visit) for visit in permutations(points))


def shortest_visit_back(space, points: List[Pos]):
    graph = build_graph(space, points)
    start = points[0]
    points = points[1:]

    def visit_length(order: List[Pos]):
        prev = start
        length = 0
        for point in order + (start,):
            length += next(n for v, n in graph.neighbors_of(prev) if v == point)
            prev = point
        return length

    return min(visit_length(visit) for visit in permutations(points))


def main(data: str):
    space, points = parse_map(data)
    yield shortest_visit(space, points)
    yield shortest_visit_back(space, points)
