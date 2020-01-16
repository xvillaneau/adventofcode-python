from typing import List, Callable

from libaoc.vectors import Vect2D, Direction


MOVES = {
    'U': Direction.Up,
    'D': Direction.Down,
    'L': Direction.Left,
    'R': Direction.Right,
}


def apply_line(line: str, start: Vect2D, check: Callable[[Vect2D], bool]):

    assert check(start)
    pos = start

    for char in line:
        prev_pos = pos
        pos += MOVES[char].vector
        if not check(pos):
            pos = prev_pos

    return pos


def get_code(lines: List[str], start: Vect2D,
             check: Callable[[Vect2D], bool],
             conv: Callable[[Vect2D], str]):
    code = []
    pos = start
    for line in lines:
        pos = apply_line(line, pos, check)
        code.append(conv(pos))
    return ''.join(code)


def is_numpad(vect: Vect2D):
    return abs(vect.x) <= 1 and abs(vect.y) <= 1


def is_weirdpad(vect: Vect2D):
    return abs(vect.x) + abs(vect.y) <= 2


def conv_numpad(vect: Vect2D):
    if not is_numpad(vect):
        raise ValueError(f'{vect} is not a numpad position')
    return str(5 - 3 * vect.y + vect.x)


def conv_weirdpad(vect: Vect2D):
    if not is_weirdpad(vect):
        raise ValueError(f'{vect} is not a weirdpad position')
    x, y = vect
    if y == 2:
        return '1'
    elif y == 1:
        return str(x + 3)
    elif y == 0:
        return str(x + 7)
    elif y == -1:
        return ['A', 'B', 'C'][x + 1]
    else:
        return 'D'


def get_num_code(lines: List[str]):
    return get_code(lines, Vect2D(0, 0), is_numpad, conv_numpad)


def get_weird_code(lines: List[str]):
    return get_code(lines, Vect2D(-2, 0), is_weirdpad, conv_weirdpad)


def main(data: str):
    lines = data.splitlines()
    yield get_num_code(lines)
    yield get_weird_code(lines)
