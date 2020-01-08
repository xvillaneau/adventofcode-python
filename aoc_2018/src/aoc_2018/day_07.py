
from dataclasses import dataclass
from collections import defaultdict
import re
from typing import Union

RE_DEPENDENCY = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin.')

TEST = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".strip().splitlines()


def read_deps(lines):
    deps = defaultdict(set)
    all_steps = set([])
    for l in lines:
        depends, dependent = RE_DEPENDENCY.search(l).groups()
        deps[dependent].add(depends)
        all_steps |= {depends, dependent}
    for first_step in all_steps - set(deps):
        deps[first_step] = set([])
    return dict(deps)


@dataclass
class Worker:
    step: Union[str, None]
    remaining: int


def multi_run(lines, workers=5, delay=60):

    deps = read_deps(lines)
    workers = [Worker(None, 0) for _ in range(workers)]
    done, time = [], 0

    while True:

        # Check work done, free the workers
        done_now, in_progress = set([]), set([])
        for w in workers:
            if w.remaining > 0:
                in_progress.add(w.step)
            elif w.step is not None:
                done_now.add(w.step)
                deps.pop(w.step)
                w.step = None

        # Add the done work to the output, check for end of process
        done.extend(sorted(done_now))
        if not in_progress and not deps:
            break

        # Give work to workers
        todo = {c for c, d in deps.items() if not d - set(done)} - in_progress
        for w in workers:
            if not todo:
                break
            if w.step is not None:
                continue
            w.step = min(todo)
            todo.remove(w.step)
            if delay >= 0:
                w.remaining = delay + ord(w.step) - 64
            else:
                w.remaining = 1

        # Update the timers
        for w in workers:
            if w.remaining > 0:
                w.remaining -= 1
        time += 1

    return ''.join(done), time


def main(data: str):
    lines = data.splitlines()
    yield multi_run(lines, 1, -1)[0]
    yield multi_run(lines)[1]
