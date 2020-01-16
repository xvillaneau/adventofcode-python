from typing import Tuple, List, Optional

Diagram = List[str]
Vector = Tuple[int, int]

D_UP = (-1, 0)
D_DOWN = (1, 0)
D_LEFT = (0, -1)
D_RIGHT = (0, 1)


def find_start(diagram: Diagram) -> Vector:
    for i, l in enumerate(diagram):
        try:
            return i, next(i for i, c in enumerate(l) if c != ' ')
        except StopIteration:
            pass


def reverse(direction: Vector) -> Vector:
    x, y = direction
    return -x, -y


def move(pos: Vector, direction: Vector) -> Vector:
    x, y = pos
    u, v = direction
    return x + u, y + v


def read(diagram: Diagram, pos: Vector) -> str:
    x, y = pos
    try:
        return diagram[x][y]
    except IndexError:
        return ' '


def turn(diagram: Diagram, pos: Vector, incoming_dir: Vector) -> Optional[Vector]:
    x, y = pos

    def _try_pos(a, b):
        return read(diagram, (a, b)) != ' '

    neighbors = {
        D_UP: _try_pos(x - 1, y),
        D_DOWN: _try_pos(x + 1, y),
        D_LEFT: _try_pos(x, y - 1),
        D_RIGHT: _try_pos(x, y + 1)
    }
    next_neighbors = set(vect for vect, test in neighbors.items() if test)
    next_neighbors.difference_update({reverse(incoming_dir)})

    if not next_neighbors:
        return None
    assert len(next_neighbors) == 1
    return next_neighbors.pop()


def follow_path(diagram: Diagram):

    pos = find_start(diagram)
    direction = D_DOWN
    count = 1

    while True:
        val = read(diagram, pos)
        if val.isalpha():
            yield val, count
        if read(diagram, move(pos, direction)) == ' ':
            direction = turn(diagram, pos, direction)
            if direction is None:
                return
        pos = move(pos, direction)
        count += 1


def main(data: str):
    follower = follow_path(data.splitlines())
    res = list(follower)
    yield ''.join(c for c, _ in res)
    yield max(i for _, i in res)
