from collections import defaultdict
import re
from typing import Dict, List, Set

Rules = Dict[str, Dict[str, int]]


def parse_rules(rules: List[str]) -> Rules:
    out = {}
    for line in rules:
        container, _, contents = line.partition(" bags contain ")
        if contents == "no other bags.":
            out[container] = {}
            continue
        bags = {}
        for rule in contents.split(', '):
            num, color = re.match(r'^(\d+) (\w+ \w+) ', rule).groups()
            bags[color] = int(num)
        out[container] = bags
    return out


def reverse_rules(rules: Rules) -> Dict[str, Set[str]]:
    reverse = defaultdict(set)
    for container, contents in rules.items():
        for color in contents:
            reverse[color].add(container)
    return reverse


def contained_by(rules: Rules, color: str) -> Set[str]:
    containers = reverse_rules(rules)
    visited, frontier = set(), {color}
    while frontier:
        color = frontier.pop()
        for container in containers.get(color, ()):
            if container not in visited:
                visited.add(container)
                frontier.add(container)
    return visited


def contains(rules: Rules, color: str) -> int:
    def _contains(col: str):
        return 1 + sum(n * _contains(c) for c, n in rules[col].items())
    return _contains(color) - 1


def main(data):
    rules = parse_rules(data.splitlines())
    yield len(contained_by(rules, "shiny gold"))
    yield contains(rules, "shiny gold")
