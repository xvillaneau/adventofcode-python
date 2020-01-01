from itertools import combinations
from dataclasses import dataclass
import re
from typing import List, Set

from libaoc.graph import WeightedGraph

RE_LINE = re.compile(r"^(\w+) to (\w+) = (\d+)$")
INF = float('inf')

def make_graph(data: List[str]) -> WeightedGraph[str]:
    places = {}
    graph = WeightedGraph([])

    for line in data:
        _from, _to, _dist = RE_LINE.match(line).groups()
        if _from not in places:
            places[_from] = graph.add_vertex(_from)
        if _to not in places:
            places[_to] = graph.add_vertex(_to)
        graph.add_edge(places[_from], places[_to], int(_dist))

    return graph

@dataclass
class RouteNode:
    current: int
    destination: int
    length: float
    graph: WeightedGraph
    visited: Set[int]

    @classmethod
    def initial(cls, start: int, destination: int, graph: WeightedGraph):
        path = [-1] * graph.vertex_count
        path[start] = 0
        return cls(start, destination, 0, graph, {start})

    @property
    def complete(self):
        return len(self.visited) == self.graph.vertex_count

    def next_routes(self):
        if self.complete:
            return []
        result = []
        for edge in self.graph.edges_at(self.current):
            if edge.v in self.visited:
                continue
            result.append(RouteNode(
                edge.v,
                self.destination,
                self.length + edge.weight,
                self.graph,
                self.visited | {edge.v}
            ))
        return result

def shortest_delivery(graph: WeightedGraph):
    result, shortest = None, INF

    for u, v in combinations(range(graph.vertex_count), 2):
        stack = [RouteNode.initial(u, v, graph)]
        while stack:
            route = stack.pop()
            if route.length > shortest:
                continue
            if route.complete:
                result = route
                shortest = route.length
            else:
                stack.extend(route.next_routes())
    return result

def longest_delivery(graph: WeightedGraph):
    result, longest = None, 0

    for u, v in combinations(range(graph.vertex_count), 2):
        stack = [RouteNode.initial(u, v, graph)]
        while stack:
            route = stack.pop()
            if route.complete and route.length > longest:
                result = route
                longest = route.length
            else:
                stack.extend(route.next_routes())
    return result


def part_1(data):
    return shortest_delivery(make_graph(data)).length

def part_2(data):
    return longest_delivery(make_graph(data)).length


# Tests

TEST_DATA = [
    "London to Dublin = 464",
    "London to Belfast = 518",
    "Dublin to Belfast = 141",
]

def test_make_graph():
    graph = make_graph(TEST_DATA)

    london = graph.index_of("London")
    assert ("Dublin", 464) in graph.neighbors_of(london)
    assert ("Belfast", 518) in graph.neighbors_of(london)
    dublin = graph.index_of("Dublin")
    assert ("London", 464) in graph.neighbors_of(dublin)
    assert ("Belfast", 141) in graph.neighbors_of(dublin)
    belfast = graph.index_of("Belfast")
    assert ("London", 518) in graph.neighbors_of(belfast)
    assert ("Dublin", 141) in graph.neighbors_of(belfast)

def test_shortest_delivery():
    graph = make_graph(TEST_DATA)
    assert shortest_delivery(graph).length == 605


def main(data: str):
    lines = data.splitlines()
    yield part_1(lines)
    yield part_2(lines)

