from typing import List, FrozenSet, Dict, Tuple, Set
import re

Links = Dict[int, FrozenSet[int]]


def parse_input(lines: List[str]) -> Links:

    def _line_tuple(line: str) -> Tuple[int, FrozenSet[int]]:
        res = re.match(r'([0-9]+) <-> ([\s,0-9]+)', line)
        if res is None:
            raise ValueError(f"Can't parse {line}")
        n, rels = res.groups()
        return int(n), frozenset(int(i) for i in rels.split(','))

    return dict(_line_tuple(l) for l in lines if l.strip())


def explore_links(links: Links, start: int) -> Set[int]:

    assert start in links
    explored = {start}
    frontier = set(links[start]) - explored

    while frontier:
        new = frontier.pop()
        explored.add(new)
        frontier = (frontier | links[new]) - explored

    return explored


def all_groups(links: Links) -> List[Set[int]]:

    unexplored = set(links.keys())
    groups = []

    while unexplored:
        new = unexplored.pop()
        group = explore_links(links, new)
        groups.append(group)
        unexplored = unexplored - group

    return groups


def main(data: str):
    many_links = parse_input(data.splitlines())
    yield len(explore_links(many_links, 0))
    yield len(all_groups(many_links))
