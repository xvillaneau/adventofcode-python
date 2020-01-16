from typing import List, Generator, Tuple


class Component(object):

    def __init__(self, port_1: int, port_2: int):
        self.port_1 = port_1
        self.port_2 = port_2

    def __contains__(self, item: int) -> bool:
        return item == self.port_1 or item == self.port_2

    def __repr__(self):
        return f"<Component {self.port_1}/{self.port_2}"

    @property
    def strength(self):
        return self.port_1 + self.port_2

    def opposite(self, port: int) -> int:
        if port == self.port_2:
            return self.port_1
        elif port == self.port_1:
            return self.port_2
        raise ValueError(f"Port {port} not a member")


Bridge = List[Component]
Inventory = List[Component]


def read_components(lines: List[str]) -> Inventory:

    def _component(line: str) -> Component:
        elems = line.split('/')
        assert len(elems) == 2
        p1, p2 = elems
        return Component(int(p1), int(p2))

    return [_component(l) for l in lines if l.strip()]


def bridge_len(bridge: Bridge) -> int:
    return sum(c.strength for c in bridge)


def find_bridges(components: Inventory) -> Generator[Bridge, None, None]:

    def _iter_builder(head: int, comps: Inventory, bridge: Bridge):

        matches = [c for c in comps if head in c]
        for m in matches:
            n_head = m.opposite(head)
            n_comps = [c for c in comps if c is not m]
            n_bridge = bridge + [m]
            yield n_bridge
            yield from _iter_builder(n_head, n_comps, n_bridge)

    yield from _iter_builder(0, components, [])


def strongest_bridge(components: Inventory) -> Tuple[Bridge, Bridge]:

    bridges = list(find_bridges(components))
    strongest = max(bridges, key=bridge_len)
    longest_len = len(max(bridges, key=list.__len__))
    long_bridges = [b for b in bridges if len(b) == longest_len]
    longest = max(long_bridges, key=bridge_len)
    return strongest, longest


def main(data: str):
    bridges = read_components(data.splitlines())
    b1, b2 = strongest_bridge(bridges)
    yield bridge_len(b1)
    yield bridge_len(b2)
