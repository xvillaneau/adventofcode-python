from collections import deque
from heapq import heappop, heappush
from typing import Dict, Set

import numpy as np

from libaoc.files import read_full
from libaoc.graph import WeightedGraph
from libaoc.vectors import Vect2D, UNIT_VECTORS


def load_maze(data: str):
    return np.array([list(line) for line in data.strip().splitlines()])


def count_neighbors(maze):
    """Use convolution to detect intersections"""
    pattern = np.array(([0, 1, 0], [1, 0, 1], [0, 1, 0]))

    m = np.pad(maze, 1)
    view_shape = tuple(np.subtract(m.shape, maze.shape) + 1) + maze.shape
    strides = m.strides + m.strides
    sub_matrices = np.lib.stride_tricks.as_strided(m, view_shape, strides)
    filtered = np.einsum('ij,ijkl->kl', pattern, sub_matrices)

    return np.where(maze, filtered, 0)


def build_graph(maze):
    tunnels = maze != "#"

    keys_map = np.where(tunnels, maze, ".") != "."
    key_indices = np.argwhere(keys_map)
    intersections = np.argwhere((count_neighbors(tunnels) > 2) & ~keys_map)

    key_names = maze[tuple(key_indices.transpose())]
    vertices = list(key_names) + [f"_{x:02}_{y:02}" for x, y in intersections]
    nodes = {Vect2D(*p): i for i, p in enumerate(np.concatenate((key_indices, intersections)))}

    def successors(position: Vect2D):
        return [
            position + move
            for move in UNIT_VECTORS
            if tunnels[tuple(position + move)]
        ]

    graph = WeightedGraph(vertices)
    distances = np.where(tunnels, 0, -10)

    origin = Vect2D(*np.argwhere(maze == "@")[0])
    explored = {origin}
    pairs_explored = set()
    frontier = deque([(origin, origin, 0)])

    while frontier:
        pos, path_start, distance = frontier.popleft()

        if pos != path_start and pos in nodes:
            graph.add_edge(nodes[pos], nodes[path_start], distance)
            pairs_explored.add(frozenset((pos, path_start)))
            frontier.appendleft((pos, pos, 0))
            continue

        for next_pos in successors(pos):
            pair = frozenset((pos, next_pos))
            if next_pos in explored and (next_pos not in nodes or pair in pairs_explored):
                continue
            explored.add(next_pos)
            frontier.append((next_pos, path_start, distance + 1))
            if next_pos not in nodes:
                distances[tuple(next_pos)] = distance + 1

    return graph


def reachable_keys(graph: WeightedGraph[str], origin: int, keys: Set[str]) -> Dict[int, int]:

    reachable = {}
    explored = {origin: 0}
    frontier = [(origin, 0)]

    while frontier:
        vertex_id, distance = frontier.pop()
        vertex = graph[vertex_id]

        if vertex.isalpha() and vertex.lower() not in keys:
            if vertex.islower():
                reachable[vertex_id] = distance
            continue

        for edge in graph.edges_at(vertex_id):
            next_id, next_dist = edge.v, distance + edge.weight
            if next_id in explored and explored[next_id] <= next_dist:
                continue
            explored[next_id] = next_dist
            frontier.append((next_id, next_dist))

    return reachable


def find_shortest_path(graph: WeightedGraph[str]):
    start_index = graph.index_of("@")
    all_keys = {name for name in graph if name.islower()}

    frontier = [(0, [start_index], set())]
    explored = {(start_index, ""): 0}

    while frontier:

        distance, path, keys = heappop(frontier)
        if keys == all_keys:
            return distance

        for key_id, key_dist in reachable_keys(graph, path[-1], keys).items():
            new_distance = distance + key_dist
            new_keys = keys | {graph[key_id]}
            state = key_id, ''.join(new_keys)
            if state in explored and explored[state] <= new_distance:
                continue
            explored[state] = new_distance
            heappush(frontier, (new_distance, path + [key_id], new_keys))


def day_18_part_1(data: str):
    maze = load_maze(data)
    graph = build_graph(maze)
    return find_shortest_path(graph)


if __name__ == '__main__':
    from libaoc import simple_main
    simple_main(2019, 18, read_full, day_18_part_1)
