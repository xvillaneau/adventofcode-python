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


def count_paths(rooms: dict[str, Room]) -> int:

    def _count(head: Room, visited: frozenset[Room]) -> int:
        paths = 0
        for room in head.neighbors:
            if room.name == "start":
                continue
            elif room.name == "end":
                paths += 1
            elif room.is_small:
                if room in visited:
                    continue
                paths += _count(room, visited | {room})
            else:
                paths += _count(room, visited)
        return paths

    return _count(rooms["start"], frozenset())


def count_more_paths(rooms: dict[str, Room]) -> int:

    def _count(head: Room, visited: frozenset[Room], has_double: bool):
        paths = 0
        for room in head.neighbors:
            if room.name == "start":
                continue
            if room.name == "end":
                paths += 1
            elif room.is_small:
                if has_double and room in visited:
                    continue
                next_double = has_double or room in visited
                paths += _count(room, visited | {room}, next_double)
            else:
                paths += _count(room, visited, has_double)
        return paths

    return _count(rooms["start"], frozenset(), False)


def main(data: str):
    rooms = parse_map(data)
    yield count_paths(rooms)
    yield count_more_paths(rooms)
