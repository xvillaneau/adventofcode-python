from typing import List
from libaoc.parsers import parse_integer_list

def _combinations(containers: List[int], target=150, total=0, n_cont=0):
    if total == target:
        yield n_cont
        return
    if not containers:
        return
    container = containers.pop()
    if total + container <= target:
        yield from _combinations(containers, target, total + container, n_cont + 1)
        yield from _combinations(containers, target, total, n_cont)
    containers.append(container)

def count_container_combinations(containers: List[int], target=150):
    containers = list(sorted(containers, reverse=True))
    combinations = list(_combinations(containers, target))
    smallest = min(combinations)
    return len(combinations), combinations.count(smallest)


def main(data: str):
    yield from count_container_combinations(parse_integer_list(data))
