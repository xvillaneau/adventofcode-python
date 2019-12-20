from dataclasses import dataclass
from heapq import heappop, heappush
from typing import TypeVar, Generic, List, Tuple, Callable, Iterable

V = TypeVar("V")


@dataclass
class WeightedEdge:
    u: int
    v: int
    weight: int

    def __reversed__(self):
        return WeightedEdge(self.v, self.u, self.weight)

    def __lt__(self, other: 'WeightedEdge'):
        return self.weight < other.weight

    def __repr__(self):
        return f"WeightedEdge({self.u}, {self.v}, {self.weight})"

    def __str__(self):
        return f"{self.u} {self.weight}> {self.v}"


class WeightedGraph(Generic[V]):
    def __init__(self, vertices: List[V] = ()) -> None:
        self._vertices: List[V] = vertices or []
        self._edges: List[List[WeightedEdge]] = [[] for _ in vertices]

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)

    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges))

    def add_edge(self, u: int, v: int, weight: int) -> None:
        edge = WeightedEdge(u, v, weight)
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(reversed(edge))

    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([])
        return self.vertex_count - 1

    def index_of(self, vertex: V):
        return self._vertices.index(vertex)

    def neighbors_of(self, index: int) -> List[V]:
        return [(self[e.v], e.weight) for e in self.edges_at(index)]

    def edges_at(self, index: int) -> List[WeightedEdge]:
        return self._edges[index]

    def __getitem__(self, item):
        return self._vertices[item]

    def __repr__(self):
        desc = ""
        for i in range(self.vertex_count):
            desc += f"{self[i]} -> {self.neighbors_of(i)}\n"
        return desc


class HWeightedGraph(WeightedGraph, Generic[V]):
    """
    Convenient subset of weighted graph, where vertices are assumed to
    be hashable. This allows the indices to be abstracted at little cost.
    """
    def __init__(self, vertices: List[V] = ()) -> None:
        super().__init__(vertices)
        self._vx_dict = {v: i for i, v in enumerate(self._vertices)}

    def __contains__(self, item):
        return item in self._vx_dict

    def add_vertex(self, vertex: V) -> int:
        if vertex in self._vx_dict:
            raise ValueError(f"Vertex {vertex} is already in the graph")
        vertex_id = super().add_vertex(vertex)
        self._vx_dict[vertex] = vertex_id
        return vertex_id

    def add_edge(self, u: V, v: V, weight: int) -> None:
        u, v = self.index_of(u), self.index_of(v)
        super().add_edge(u, v, weight)

    def index_of(self, vertex: V):
        return self._vx_dict[vertex]

    def neighbors_of(self, vertex: V) -> List[Tuple[V, int]]:
        return [(self[e.v], e.weight) for e in self.edges_at(vertex)]

    def edges_at(self, vertex: V) -> List[WeightedEdge]:
        return self._edges[self.index_of(vertex)]

    def __repr__(self):
        desc = ""
        for v in self._vx_dict:
            desc += f"{v!r} -> {self.neighbors_of(v)}\n"
        return desc


T = TypeVar("T")


def build_graph(
    initial_nodes: List[T],
    is_vertex: Callable[[T], bool],
    as_vertex: Callable[[T], V],
    successors: Callable[[T], Iterable[Tuple[T, int]]],
) -> HWeightedGraph[V]:

    assert all(is_vertex(init) for init in initial_nodes)
    frontier = [(0, init, init) for init in initial_nodes]
    nodes_explored = {(init, init): 0 for init in initial_nodes}
    edges_explored = {}

    graph = HWeightedGraph([as_vertex(init) for init in initial_nodes])

    while frontier:
        cost, start, current = heappop(frontier)

        if is_vertex(current) and current != start:
            if (vertex := as_vertex(current)) not in graph:
                graph.add_vertex(vertex)
                heappush(frontier, (0, current, current))
            pair = frozenset((as_vertex(start), as_vertex(current)))
            if pair not in edges_explored or edges_explored[pair] > cost:
                edges_explored[pair] = cost
            continue

        for next_state, distance in successors(current):
            next_cost = cost + distance
            node = (start, next_state)
            if node in nodes_explored and nodes_explored[node] <= next_cost:
                continue
            nodes_explored[node] = next_cost
            heappush(frontier, (next_cost, start, next_state))

    for (u, v), weight in edges_explored.items():
        graph.add_edge(u, v, weight)

    return graph
