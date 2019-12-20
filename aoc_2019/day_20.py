from collections import deque
from heapq import heappush, heappop
import re
from typing import Dict, Tuple

import numpy as np

from libaoc.graph import HWeightedGraph
from libaoc.matrix import convolve_2d_3x3
from libaoc.vectors import Vect2D, UP, LEFT, DOWN, RIGHT, UNIT_VECTORS

Portal = Tuple[str, bool]


def load_maze(data: str):
    lines = [line for line in data.splitlines() if line.strip()]
    max_len = max(len(line) for line in lines)
    return np.array([list(f"{line:{max_len}}") for line in lines])


RE_PORTAL = re.compile(r"([A-Z])[^A-Z]*([A-Z])")

def find_portals(maze):
    walls = np.where(maze == ".", " ", maze) != " "
    pattern = np.array([[-1, 1, -1], [-1, 1, -1], [1, -1, 1]])

    portals = []
    for i, v in enumerate((RIGHT, UP, LEFT, DOWN)):
        coords = np.argwhere(convolve_2d_3x3(walls, np.rot90(pattern, i)) == 4)
        for x, y in coords:
            label = ''.join(maze[x - 1:x + 2, y - 1:y + 2].reshape(9))
            label = re.sub(r"[\s#.]", "", label)
            pos = Vect2D(x, y) + v
            portals.append((pos, label))

    return portals


def process_maze(maze):
    portals = find_portals(maze)

    voids = ~(maze == "#")

    offset = Vect2D(0, 0)
    if np.all(voids[:2, :]):
        offset += Vect2D(-2, 0)
        maze = np.delete(maze, slice(None, 2), axis=0)
    if np.all(voids[:, :2]):
        offset += Vect2D(0, -2)
        maze = np.delete(maze, slice(None, 2), axis=1)
    if np.all(voids[-2:, :]):
        maze = np.delete(maze, slice(-2, None), axis=0)
    if np.all(voids[:, -2:]):
        maze = np.delete(maze, slice(-2, None), axis=1)

    donut = (maze == ".") | (maze == "#")
    maze = np.where(donut, maze, "#") == "."
    sx, sy = maze.shape

    new_portals = {}
    for pos, name in portals:
        pos = pos + offset
        outer = pos.x in (0, sx - 1) or pos.y in (0, sy - 1)
        new_portals[(name, outer)] = pos

    return maze, new_portals


def model_paths(maze, portals: Dict[Portal, Vect2D]) -> HWeightedGraph:

    graph = HWeightedGraph()

    for (name, outer), _ in portals.items():
        graph.add_vertex((name, outer))
        if (name, not outer) in graph:
            graph.add_edge((name, outer), (name, not outer), 1)

    sx, sy = maze.shape
    def successors(_pos: Vect2D):
        for v in UNIT_VECTORS:
            _new = _pos + v
            if 0 <= _new.x < sx and 0 <= _new.y < sy and maze[tuple(_new)]:
                yield _new

    pairs_explored = set()
    portals_waiting = set(portals)
    portals_by_pos = {pos: port for port, pos in portals.items()}

    while portals_waiting:
        start_portal = portals_waiting.pop()
        start_pos = portals[start_portal]

        found = []
        frontier = deque([start_pos])
        explored = {start_pos: 0}

        while frontier:
            position = frontier.popleft()

            if position != start_pos and position in portals_by_pos:
                new_portal = portals_by_pos[position]
                if frozenset((start_portal, new_portal)) in pairs_explored:
                    continue
                graph.add_edge(start_portal, new_portal, explored[position])
                pairs_explored.add(frozenset((start_portal, new_portal)))
                found.append(new_portal)
                continue

            next_dist = explored[position] + 1
            for next_pos in successors(position):
                if next_pos in explored and explored[next_pos] <= next_dist:
                    continue
                explored[next_pos] = next_dist
                frontier.append(next_pos)

        if len(found) == 1:
            portals_waiting.discard(found[0])

    return graph


def shortest_path(graph: HWeightedGraph):
    start, end = ("AA", True), ("ZZ", True)

    frontier = [(0, start)]
    explored = {start: 0}

    while frontier:
        distance, portal = heappop(frontier)
        if portal == end:
            return distance

        for neighbor, dist in graph.neighbors_of(portal):
            next_dist = distance + dist
            if neighbor in explored and explored[neighbor] <= next_dist:
                continue
            explored[neighbor] = next_dist
            heappush(frontier, (next_dist, neighbor))


def day_20(data: str):
    maze, portals = process_maze(load_maze(data))
    graph = model_paths(maze, portals)
    yield shortest_path(graph)


if __name__ == '__main__':
    from libaoc import files, iter_main
    iter_main(2019, 20, files.read_full, day_20)
