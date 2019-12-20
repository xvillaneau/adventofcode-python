from heapq import heappop, heappush
from itertools import chain
from typing import Dict, List, Set

import numpy as np

from libaoc.files import read_full
from libaoc.graph import HWeightedGraph, build_graph
from libaoc.matrix import load_string_matrix
from libaoc.vectors import Vect2D, UNIT_VECTORS

Graph = HWeightedGraph[str]

PATTERN = np.array(([0, 1, 0], [1, 0, 1], [0, 1, 0]))


def build_graphs(maze) -> List[Graph]:
    """
    Given the maze as a string, build a graph of the shortest distances
    between the start and all doors/keys.

    This function works in three steps:
     1. Identify the tunnels, junctions and objects in the maze
     2. Do a breadth-first walk through all the tunnels, and build a
        graph of distances between all junctions and objects (one per
        starting point; we assume the resulting graphs are distinct).
     3. Use that graph to run a second BFS and build a new graph with
        only the points of interest (start, keys, doors).
    """
    # Boolean map of th tunnels ("not walls")
    tunnels = maze != "#"

    # Build a set of all vertices for a first graph: junctions and objects
    objects_map = np.where(tunnels, maze, ".") != "."
    nodes = {Vect2D(*p): maze[tuple(p)] for p in np.argwhere(objects_map)}

    def successors(_pos: Vect2D):
        for v in UNIT_VECTORS:
            _new = _pos + v
            if tunnels[tuple(_new)]:
                yield _new, 1

    def make_graph(origin: Vect2D) -> Graph:
        return build_graph(
            [origin],
            nodes.__contains__,
            nodes.__getitem__,
            successors,
        )

    return [make_graph(Vect2D(*p)) for p in np.argwhere(maze == "@")]


def reachable_keys(graph: Graph, position: str, keys: Set[str]) -> Dict[str, int]:

    reachable = {}
    explored = {position: 0}
    frontier = [(0, position)]

    while frontier:
        cost, vertex = frontier.pop()

        if vertex.isalpha() and vertex.lower() not in keys:
            if vertex.islower():
                reachable[vertex] = cost
            continue

        for neighbor, distance in graph.neighbors_of(vertex):
            next_cost = cost + distance
            if neighbor in explored and explored[neighbor] <= next_cost:
                continue
            explored[neighbor] = next_cost
            frontier.append((next_cost, neighbor))

    return reachable


def find_shortest_path(graph: Graph):
    all_keys = {name for name in graph if name.islower()}

    frontier = [(0, ["@"], set())]
    explored = {("@", frozenset()): 0}

    while frontier:

        cost, path, keys = heappop(frontier)
        if keys == all_keys:
            return cost

        for key, distance in reachable_keys(graph, path[-1], keys).items():
            new_distance = cost + distance
            new_keys = keys | {key}
            state = key, frozenset(new_keys)
            if state in explored and explored[state] <= new_distance:
                continue
            explored[state] = new_distance
            heappush(frontier, (new_distance, path + [key], new_keys))


def solve_four_robots(graph_1: Graph, graph_2: Graph, graph_3: Graph, graph_4: Graph):

    all_keys = {
        name
        for graph in (graph_1, graph_2, graph_3, graph_4)
        for name in graph
        if name.islower()
    }

    init = (frozenset(), "@", "@", "@", "@")
    frontier = [(0, init)]
    explored = {init: 0}

    while frontier:
        distance, (keys, pos_1, pos_2, pos_3, pos_4) = heappop(frontier)
        if keys == all_keys:
            return distance

        states_1 = (
            ((keys | {k1}, k1, pos_2, pos_3, pos_4), distance + d1)
            for k1, d1 in reachable_keys(graph_1, pos_1, keys).items()
        )
        states_2 = (
            ((keys | {k2}, pos_1, k2, pos_3, pos_4), distance + d2)
            for k2, d2 in reachable_keys(graph_2, pos_2, keys).items()
        )
        states_3 = (
            ((keys | {k3}, pos_1, pos_2, k3, pos_4), distance + d3)
            for k3, d3 in reachable_keys(graph_3, pos_3, keys).items()
        )
        states_4 = (
            ((keys | {k4}, pos_1, pos_2, pos_3, k4), distance + d4)
            for k4, d4 in reachable_keys(graph_4, pos_4, keys).items()
        )

        for state, new_distance in chain(states_1, states_2, states_3, states_4):
            if state in explored and explored[state] <= new_distance:
                continue
            explored[state] = new_distance
            heappush(frontier, (new_distance, state))


def insert_robots(maze):
    robots = np.array([list("@#@"), list("###"), list("@#@")])
    x, y = np.argwhere(maze == "@")[0]
    new_maze = maze.copy()
    new_maze[x-1:x+2, y-1:y+2] = robots
    return new_maze


def day_18_part_1(data: str):
    maze = load_string_matrix(data)
    graphs = build_graphs(maze)
    assert len(graphs) == 1
    return find_shortest_path(graphs[0])


def day_18_part_2(data: str):
    maze = insert_robots(load_string_matrix(data))
    graphs = build_graphs(maze)
    assert len(graphs) == 4
    return solve_four_robots(*graphs)


if __name__ == '__main__':
    from libaoc import simple_main
    simple_main(2019, 18, read_full, day_18_part_1, day_18_part_2)
