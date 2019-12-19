from collections import deque
from heapq import heappop, heappush
from itertools import chain
from typing import Dict, List, Set

import numpy as np

from libaoc.files import read_full
from libaoc.graph import WeightedGraph
from libaoc.matrix import convolve_2d_3x3, load_string_matrix
from libaoc.vectors import Vect2D, UNIT_VECTORS

Graph = WeightedGraph[str]

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
    junctions = np.where(tunnels, convolve_2d_3x3(tunnels, PATTERN), 0) > 2
    nodes = {Vect2D(*p) for p in np.argwhere(junctions | objects_map)}

    def make_graph(origin: Vect2D) -> Graph:

        explored = {origin}
        pairs_explored = set()
        frontier = deque([(origin, origin, 0)])

        graph = WeightedGraph(["@"])
        node_ids: Dict[Vect2D, int] = {origin: 0}

        while frontier:
            pos, path_start, distance = frontier.popleft()

            if pos != path_start and pos in nodes:

                if pos not in node_ids:
                    value = maze[tuple(pos)]
                    vertex_name = value if value != "." else f"_{pos.x:02}_{pos.y:02}"
                    node_ids[pos] = graph.add_vertex(vertex_name)

                graph.add_edge(node_ids[pos], node_ids[path_start], distance)
                pairs_explored.add(frozenset((pos, path_start)))
                frontier.appendleft((pos, pos, 0))
                continue

            for move in UNIT_VECTORS:
                next_pos = pos + move
                if not tunnels[tuple(next_pos)]:
                    continue
                if next_pos not in nodes and next_pos in explored:
                    continue
                pair = frozenset((pos, next_pos))
                if next_pos in nodes and pair in pairs_explored:
                    continue

                explored.add(next_pos)
                frontier.append((next_pos, path_start, distance + 1))

        optimize = False
        if not optimize:
            return graph

        # WIP
        opt_graph = WeightedGraph(["@"])
        return opt_graph

    return [make_graph(Vect2D(*p)) for p in np.argwhere(maze == "@")]


def reachable_keys(graph: Graph, position: int, keys: Set[str]) -> Dict[int, int]:

    reachable = {}
    explored = {position: 0}
    frontier = [(position, 0)]

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


def find_shortest_path(graph: Graph):
    start_index = graph.index_of("@")
    all_keys = {name for name in graph if name.islower()}

    frontier = [(0, [start_index], set())]
    explored = {(start_index, frozenset()): 0}

    while frontier:

        distance, path, keys = heappop(frontier)
        if keys == all_keys:
            return distance

        for key_id, key_dist in reachable_keys(graph, path[-1], keys).items():
            new_distance = distance + key_dist
            new_keys = keys | {graph[key_id]}
            state = key_id, frozenset(new_keys)
            if state in explored and explored[state] <= new_distance:
                continue
            explored[state] = new_distance
            heappush(frontier, (new_distance, path + [key_id], new_keys))


def solve_four_robots(graph_1: Graph, graph_2: Graph, graph_3: Graph, graph_4: Graph):

    start_1 = graph_1.index_of("@")
    start_2 = graph_2.index_of("@")
    start_3 = graph_3.index_of("@")
    start_4 = graph_4.index_of("@")

    all_keys = {
        name
        for graph in (graph_1, graph_2, graph_3, graph_4)
        for name in graph
        if name.islower()
    }

    frontier = [(0, frozenset(), start_1, start_2, start_3, start_4)]
    explored = {(frozenset(), start_1, start_2, start_3, start_4): 0}

    while frontier:
        distance, keys, pos_1, pos_2, pos_3, pos_4 = heappop(frontier)
        if keys == all_keys:
            return distance

        states_1 = (
            ((keys | {graph_1[k1]}, k1, pos_2, pos_3, pos_4), distance + d1)
            for k1, d1 in reachable_keys(graph_1, pos_1, keys).items()
        )
        states_2 = (
            ((keys | {graph_2[k2]}, pos_1, k2, pos_3, pos_4), distance + d2)
            for k2, d2 in reachable_keys(graph_2, pos_2, keys).items()
        )
        states_3 = (
            ((keys | {graph_3[k3]}, pos_1, pos_2, k3, pos_4), distance + d3)
            for k3, d3 in reachable_keys(graph_3, pos_3, keys).items()
        )
        states_4 = (
            ((keys | {graph_4[k4]}, pos_1, pos_2, pos_3, k4), distance + d4)
            for k4, d4 in reachable_keys(graph_4, pos_4, keys).items()
        )

        for state, new_distance in chain(states_1, states_2, states_3, states_4):
            if state in explored and explored[state] <= new_distance:
                continue
            explored[state] = new_distance
            heappush(frontier, (new_distance, *state))


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
