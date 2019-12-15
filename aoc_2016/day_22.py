from itertools import combinations
import re
from typing import NamedTuple, Dict, Generator, Tuple

from libaoc.vectors import Vect2D, UP, LEFT, DOWN, RIGHT

RE_NODE = re.compile(r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T")


class StorageNode(NamedTuple):
    position: Vect2D
    size: int
    used: int

    @property
    def avail(self):
        return self.size - self.used

    def viable_with(self, other: 'StorageNode'):
        if not self.used:
            return False
        if self.position == other.position:
            return False
        return self.used <= other.avail


def parse_nodes(df_output):
    nodes = {}
    for line in df_output[2:]:
        x, y, size, used, avail = map(int, RE_NODE.match(line).groups())
        pos = Vect2D(x, y)
        assert size == used + avail
        nodes[pos] = StorageNode(pos, size, used)
    return nodes


def viable_pairs(
    nodes: Dict[Vect2D, StorageNode]
) -> Generator[Tuple[StorageNode, StorageNode], None, None]:
    for node_a, node_b in combinations(nodes.values(), 2):
        if node_a.viable_with(node_b):
            yield node_a, node_b
        if node_b.viable_with(node_a):
            yield node_b, node_a


def day_20(df_output):
    nodes = parse_nodes(df_output)
    yield sum(1 for _ in viable_pairs(nodes))
    yield None


if __name__ == '__main__':
    from libaoc import iter_main, files
    iter_main(2016, 22, files.read_lines, day_20)
