import re
import numpy as np


def find(letter: str, string) -> int:
    return np.argwhere(string == letter)[0, 0]


def swap_pos(x: int, y: int, string):
    ids = np.indices(string.shape)[0]
    ids[x], ids[y] = y, x
    return string[ids]


def swap_letters(x: str, y: str, string):
    x = find(x, string)
    y = find(y, string)
    return swap_pos(x, y, string)


def rotate_right(x: int, string):
    return np.roll(string, x)


def rotate_based(x: str, string, reverse=False):
    x = find(x, string)
    if not reverse:
        return rotate_right(1 + x + (x >= 4), string)
    ids = np.indices(string.shape)[0]
    ids = (ids * 2 + 1 + (ids >= 4)) % len(ids)
    prev_id = np.argwhere(ids == x)[0, 0]
    return rotate_right(prev_id - x, string)


def reverse_positions(x: int, y: int, string):
    ids = np.indices(string.shape)[0]
    ids[x:y+1] = np.flip(ids[x:y+1])
    return string[ids]


def move_position(x: int, y: int, string):
    ids = np.indices(string.shape)[0]
    if y > x:
        ids[x:y+1] = np.roll(ids[x:y+1], -1)
    elif y < x:
        ids[y:x+1] = np.roll(ids[y:x+1], 1)
    else:
        return string
    return string[ids]


def scramble(instructions, start="abcdefgh", reverse=False):
    string = np.array(list(start))
    for line in instructions[::(-1 if reverse else 1)]:
        if m := re.match(r"swap position (\d) with position (\d)", line):
            x, y = m.groups()
            string = swap_pos(int(x), int(y), string)
        elif m := re.match(r"swap letter (\w) with letter (\w)", line):
            string = swap_letters(*m.groups(), string)
        elif m := re.match(r"rotate (left|right) (\d) steps?", line):
            d, x = m.groups()
            x = int(x) * (1 if d == "right" else -1) * (-1 if reverse else 1)
            string = rotate_right(x, string)
        elif m := re.match(r"rotate based on position of letter (\w)", line):
            string = rotate_based(m.group(1), string, reverse)
        elif m := re.match(r"reverse positions (\d) through (\d)", line):
            x, y = m.groups()
            string = reverse_positions(int(x), int(y), string)
        elif m := re.match(r"move position (\d) to position (\d)", line):
            x, y = m.groups()
            if reverse:
                x, y = y, x
            string = move_position(int(x), int(y), string)
        else:
            raise ValueError(f"Unknown line: {line!r}")
    return ''.join(string)


def main(data: str):
    lines = data.splitlines()
    yield scramble(lines)
    yield scramble(lines, start="fbgdceah", reverse=True)
