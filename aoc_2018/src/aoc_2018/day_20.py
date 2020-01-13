from collections import defaultdict, deque
import re
from typing import Dict, Set, Tuple

RE_SEQ = re.compile("[NESW]*[^NESW]")
Pos = Tuple[int, int]
Rooms = Dict[Pos, Set[Pos]]


def parse_input(data: str):
    path_stack = []
    fork_stack = []

    for elem in RE_SEQ.findall(data):
        seq, op = elem[:-1], elem[-1]

        if op == "^":
            path_stack.append([])

        elif op == "$":
            assert len(path_stack) == 1
            assert not fork_stack
            if seq:
                path_stack[0].append(seq)
            return path_stack[0]

        elif op == "(":
            path_stack[-1].append(seq)
            fork_stack.append([])
            path_stack.append([])

        elif op in "|)":
            path = path_stack.pop()
            if not path:
                path = seq
            elif seq:
                path.append(seq)
            fork = fork_stack.pop()
            fork.append(path)

            if op == "|":
                fork_stack.append(fork)
                path_stack.append([])
            else:
                path_stack[-1].append(fork)


def move_pos(pos: Pos, move: str):
    x, y = pos
    if move == "N":
        return x, y + 1
    elif move == "S":
        return x, y - 1
    elif move == "E":
        return x + 1, y
    elif move == "W":
        return x - 1, y
    else:
        raise ValueError


def explore_str(rooms: Rooms, path: str, start: Pos) -> Pos:
    pre_pos = start
    for move in path:
        new_pos = move_pos(pre_pos, move)
        rooms[new_pos].add(pre_pos)
        rooms[pre_pos].add(new_pos)
        pre_pos = new_pos
    return pre_pos


def explore_path(rooms: Rooms, path, start: Pos) -> Set[Pos]:
    if isinstance(path, str):
        path = [path]
    positions = {start}
    for elem in path:
        if isinstance(elem, str):
            positions = {explore_str(rooms, elem, pos) for pos in positions}
        else:
            new_pos = (explore_fork(rooms, elem, pos) for pos in positions)
            positions = set.union(*new_pos)
    return positions


def explore_fork(rooms: Rooms, fork, start: Pos) -> Set[Pos]:
    positions = set()
    for elem in fork:
        positions.update(explore_path(rooms, elem, start))
    return positions


def build_map(data: str):
    full_tree = parse_input(data)
    rooms = defaultdict(set)
    explore_path(rooms, full_tree, (0, 0))
    return rooms


def room_distances(rooms: Rooms):
    pos = (0, 0)
    frontier = deque([pos])
    visited = {pos: 0}

    while frontier:
        pos = frontier.popleft()
        next_steps = visited[pos] + 1
        for next_pos in rooms[pos]:
            if next_pos in visited:
                continue
            visited[next_pos] = next_steps
            frontier.append(next_pos)

    return visited


def furthest_room(rooms: Rooms):
    return max(room_distances(rooms).values())


def main(data: str):
    rooms = build_map(data)
    rooms_dist = room_distances(rooms)
    yield max(rooms_dist.values())
    yield sum(1 for d in rooms_dist.values() if d >= 1000)
