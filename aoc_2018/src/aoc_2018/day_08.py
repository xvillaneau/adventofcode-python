
from dataclasses import dataclass
from typing import List, Tuple

TEST = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


@dataclass
class Node:
    children: List['Node']
    metadata: List[int]


def parse_tree(numbers: List[int]) -> Tuple[Node, int]:
    n_children, n_meta = numbers[:2]
    children, index = [], 2
    for _ in range(n_children):
        child, child_len = parse_tree(numbers[index:])
        index += child_len
        children.append(child)
    meta = numbers[index:index + n_meta]
    return Node(children, meta), index + n_meta


def sum_metadata(tree: Node) -> int:
    return sum(sum_metadata(c) for c in tree.children) + sum(tree.metadata)


def value(tree: Node) -> int:
    if not tree.children:
        return sum(tree.metadata)
    return sum(value(tree.children[m - 1]) for m in tree.metadata
               if 0 < m <= len(tree.children))


def main(data: str):
    tree, _ = parse_tree([int(n) for n in data.strip().split()])
    yield sum_metadata(tree)
    yield value(tree)
