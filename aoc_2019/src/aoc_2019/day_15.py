from collections import deque
from dataclasses import dataclass

from libaoc import BaseRunner
from libaoc.vectors import Vect2D, UP, DOWN, LEFT, RIGHT
from .intcode import CodeRunner


DIRECTIONS = [
    (1, "N", UP),
    (2, "S", DOWN),
    (3, "W", LEFT),
    (4, "E", RIGHT),
]


@dataclass
class DroidPos:
    runner: CodeRunner
    position: Vect2D
    path: str = ""
    is_oxygen_system: bool = False

    def next_nodes(self):
        result = []
        for command, direction, vector in DIRECTIONS:
            runner = self.runner.copy()
            runner.send(command)
            status = next(runner)
            if not status:
                continue
            pos = DroidPos(
                runner, self.position + vector, self.path + direction, status == 2
            )
            result.append(pos)
        return result


def search_oxygen_system(code):
    start = DroidPos(CodeRunner(code), Vect2D(0, 0))
    frontier = deque((start,))
    explored = {start.position}
    ox_pos = None

    while frontier:
        node = frontier.popleft()

        if node.is_oxygen_system:
            if ox_pos is not None:
                raise RuntimeError("Found more than 1 oxygen system")
            ox_pos = node.position
            yield len(node.path)

        for child in node.next_nodes():
            if child.position in explored:
                continue
            explored.add(child.position)
            frontier.append(child)

    if ox_pos is None:
        raise RuntimeError("Oxygen system not found")

    has_oxygen = {ox_pos}
    max_oxygen_time = 0
    frontier = deque([(ox_pos, 0)])

    while frontier:
        position, ox_time = frontier.popleft()
        if ox_time > max_oxygen_time:
            max_oxygen_time = ox_time
        for _, _, v in DIRECTIONS:
            next_pos = position + v
            if next_pos not in explored or next_pos in has_oxygen:
                continue
            has_oxygen.add(next_pos)
            frontier.append((next_pos, ox_time + 1))

    yield max_oxygen_time


class AocRunner(BaseRunner):
    year = 2019
    day = 15
    parser = BaseRunner.int_list_parser(",")

    def run(self, code):
        yield from search_oxygen_system(code)
