from collections import Counter
from functools import cached_property


class Room:
    def __init__(self, name: str):
        self.name = name
        self.neighbors: set[Room] = set()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Room):
            return self.name == other.name
        return self.name == other

    def __repr__(self):
        return self.name

    @cached_property
    def is_small(self) -> bool:
        return self.name.islower()


def parse_map(data: str) -> dict[str, Room]:
    rooms = {}

    for ln in data.strip().splitlines():
        name_a, _, name_b = ln.partition("-")
        room_a = rooms.setdefault(name_a, Room(name_a))
        room_b = rooms.setdefault(name_b, Room(name_b))
        room_a.neighbors.add(room_b)
        room_b.neighbors.add(room_a)

    return rooms


def find_paths(rooms: dict[str, Room], path: tuple[Room, ...] = ()):
    if not path:
        path = (rooms["start"],)

    head: Room = path[-1]
    for room in head.neighbors:
        if room.is_small and room in path:
            continue
        if room.name == "end":
            yield (*path, room)
        else:
            yield from find_paths(rooms, (*path, room))


def count_more_paths(rooms: dict[str, Room]) -> int:

    def _count(head: Room, visited: frozenset[Room], has_double: bool):
        paths = 0
        for room in head.neighbors:
            if room.name == "start":
                continue
            if room.is_small and has_double and room in visited:
                continue
            if room.name == "end":
                paths += 1
            elif room.is_small:
                paths += _count(
                    room,
                    visited | {room},
                    has_double or room in visited,
                )
            else:
                paths += _count(room, visited, has_double)
        return paths

    return _count(rooms["start"], frozenset(), False)


def main(data: str):
    rooms = parse_map(data)
    yield sum(1 for _ in find_paths(rooms))
    yield count_more_paths(rooms)
