from dataclasses import dataclass
from collections import defaultdict
from heapq import heappop, heappush
from typing import Dict, List, Set


def read_dependencies(lines) -> Dict[str, Set[str]]:
    deps = defaultdict(set)
    all_steps = set([])

    for line in lines:
        depends, dependent = line[5], line[36]
        deps[dependent].add(depends)
        all_steps |= {depends, dependent}

    for first_step in all_steps - set(deps):
        deps[first_step] = set([])
    return dict(deps)


def update_dependencies(dependencies, frontier, value: str = ""):
    visited = []
    for key, deps in dependencies.items():
        deps.discard(value)
        if not deps:
            heappush(frontier, key)
            visited.append(key)
    for key in visited:
        dependencies.pop(key)


def solve_steps(lines: List[str]):
    dependencies = read_dependencies(lines)
    frontier, sequence = [],  ""

    update_dependencies(dependencies, frontier)
    while frontier:
        step = heappop(frontier)
        sequence += step
        update_dependencies(dependencies, frontier, step)

    return sequence


@dataclass
class Worker:
    work: str = ""
    remaining: int = 0


def multi_run(lines, workers=5, delay=60):

    dependencies = read_dependencies(lines)
    workers = [Worker() for _ in range(workers)]
    time, frontier = 0, []

    update_dependencies(dependencies, frontier)

    while frontier or dependencies:

        # Check for work that was just finished
        for worker in workers:
            if worker.work and not worker.remaining:
                update_dependencies(dependencies, frontier, worker.work)
                worker.work = ""

        # Assign work to the available workers
        for worker in workers:
            if not frontier:
                break
            if not worker.work:
                step = heappop(frontier)
                worker.work = step
                worker.remaining = delay + ord(step) - 64

        # Jump straight to the next time where work gets completed
        jump = min(w.remaining for w in workers if w.work)
        time += jump
        for worker in workers:
            if worker.work:
                worker.remaining -= jump

    return time


def main(data: str):
    lines = data.splitlines()
    yield solve_steps(lines)
    yield multi_run(lines)
