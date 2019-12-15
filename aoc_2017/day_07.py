from collections import Counter
import re
from typing import Tuple, List, Dict


def parse_line(line: str) -> Tuple[str, int, List[str]]:
    name, str_weight = re.match("([a-z]+) \(([0-9]+)\)", line).groups()

    res_children = re.search(" -> (.*)$", line)
    if res_children is None:
        children = []
    else:
        children = res_children.groups()[0].split(', ')

    return name, int(str_weight), children


def parse_file(lines: List[str]) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
    parsed_data = [parse_line(line) for line in lines if line]
    weights = dict((name, weight) for name, weight, _ in parsed_data)
    relations = dict((name, children) for name, _, children in parsed_data)
    return weights, relations


def find_root(relations: Dict[str, List[str]]):
    all_children = set(child for children in relations.values() for child in children)
    all_nodes = set(relations.keys())
    roots = all_nodes - all_children
    assert len(roots) == 1
    return roots.pop()


def weight_stack(node, weights, relations, weight_cache):
    if node in weight_cache:  # Cache the result, for speed
        return weight_cache[node]
    else:
        res = weights[node] + sum(weight_stack(child, weights, relations, weight_cache)
                                  for child in relations[node])
        weight_cache[node] = res
        return res


def is_balanced(node, weights, relations, weight_cache):
    if not relations[node]:
        return True
    child_weights = set(weight_stack(child, weights, relations, weight_cache)
                        for child in relations[node])
    return len(child_weights) == 1


def highest_unstable(weights, relations, weight_cache):
    return next(
        node for node in weights
        if not is_balanced(node, weights, relations, weight_cache)
        if all(is_balanced(child, weights, relations, weight_cache)
               for child in relations[node]))


def solve_balance(weights, relations):
    weight_cache = {}
    unstable = highest_unstable(weights, relations, weight_cache)
    assert len(relations[unstable]) > 2  # Un-solvable otherwise

    child_weight_counts = Counter([
        weight_stack(child, weights, relations, weight_cache)
        for child in relations[unstable]])
    assert len(child_weight_counts) == 2  # Only one culprit allowed

    culprit_weight = next(w for w, n in child_weight_counts.items() if n == 1)
    correct_weight = next(w for w, n in child_weight_counts.items() if n > 1)

    culprit = next(child for child in relations[unstable] if weight_cache[child] == culprit_weight)
    return culprit, weights[culprit] + (correct_weight - culprit_weight)


def day_07(process_dump: List[str]):
    ws, rels = parse_file(process_dump)
    yield find_root(rels)
    yield solve_balance(ws, rels)[1]


if __name__ == '__main__':
    from libaoc import iter_main, files
    iter_main(2017, 7, files.read_lines, day_07)
