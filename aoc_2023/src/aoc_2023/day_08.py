import functools
import itertools

from libaoc.math import merge_pulses

Nodes = dict[str, tuple[str, str]]


def parse_data(data: str) -> (str, Nodes):
    directions, _, nodes_str = data.partition('\n\n')
    nodes = {}
    for line in nodes_str.splitlines():
        nodes[line[:3]] = (line[7:10], line[12:15])
    return directions.strip(), nodes


def count_steps(directions: str, nodes: Nodes):
    node = "AAA"
    for i, d in enumerate(itertools.cycle(directions), start=1):
        left, right = nodes[node]
        node = left if d == 'L' else right
        if node == "ZZZ":
            return i


def count_ghost_steps(directions: str, nodes: Nodes):

    @functools.lru_cache(maxsize=None)
    def run_cycle(start: str) -> tuple[str, list[int]]:
        """
        Runs a full cycle of directions from a given start node,
        return the end node and the indices of exiting nodes.
        """
        node = start
        ends = []
        for i, d in enumerate(directions, start=1):
            left, right = nodes[node]
            node = left if d == 'L' else right
            if node[2] == "Z":
                ends.append(i)
        return node, ends

    def detect_loop(node: str) -> tuple[int, int, int]:
        """
        Runs the directions from a given node and looks for loops.
        Returns the start step of the loop, the length of the loop,
        and the position of the exit in the loop (there MUST be one).
        """
        visited = set()
        path = []
        while node not in visited:
            path.append(node)
            visited.add(node)
            node = run_cycle(node)[0]

        ln = len(directions)
        start_i = path.index(node)

        ends = []
        for i, node in enumerate(path[start_i:]):
            for end in run_cycle(node)[1]:
                ends.append(i * ln + end)
        assert len(ends) == 1  # Otherwise this is A LOT more complex

        return ln * start_i, ln * (len(path) - start_i), ends[0]

    # How to solve this fast: lets assume that the paths followed by ghosts
    # eventually loop back on themselves (at the same node AND at the start
    # of the directions). Once we know the period and offset of those loops,
    # we can use algebra to find the first sync step fast.
    # We *strongly* rely on the assumption that there is only one exit node
    # reached by loop. This seems to be true for the full AoC input.
    loops = [detect_loop(node) for node in nodes.keys() if node[2] == "A"]
    sync_start, sync_period = merge_pulses(*((s + e, p) for s, p, e in loops))

    # Finally, find the first real sync. Remember that ghosts may need some
    # initial steps before reaching the loops, so we need to exclude sync
    # steps that fall in that initialization.
    # We'll assume that sync won't happen outside the loops.
    offset = max(s for s, _, _ in loops)
    sync = sync_start
    while sync < offset:
        sync += sync_period
    return sync


def main(data: str):
    directions, nodes = parse_data(data)
    yield count_steps(directions, nodes)
    yield count_ghost_steps(directions, nodes)
