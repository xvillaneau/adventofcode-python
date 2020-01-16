from functools import partial
import re

import numpy as np

SCREEN_H = 6
SCREEN_W = 50

RE_RECT = re.compile(r"rect (\d+)x(\d+)")
RE_ROTR = re.compile(r"rotate row y=(\d+) by (\d+)")
RE_ROTC = re.compile(r"rotate column x=(\d+) by (\d+)")

TEST = [
    "rect 3x2",
    "rotate column x=1 by 1",
    "rotate row y=0 by 4",
    "rotate column x=1 by 1",
]


def rect(a, b, screen):
    h, w = screen.shape
    r = np.pad(np.ones((b, a)), ((0, h - b), (0, w - a)), "constant")
    return 1 * ((r + screen) > 0)


def rot_row(a, b, screen):
    s = screen.copy()
    s[a] = np.roll(s[a], b)
    return s


def rot_col(a, b, screen):
    s = screen.copy()
    s[:, a] = np.roll(s[:, a], b)
    return s


def get_instruction(line):

    if RE_RECT.search(line):
        f, m = rect, RE_RECT.search(line)
    elif RE_ROTC.search(line):
        f, m = rot_col, RE_ROTC.search(line)
    elif RE_ROTR.search(line):
        f, m = rot_row, RE_ROTR.search(line)
    else:
        raise ValueError(f"WTF is this: {line}")

    a, b = map(int, m.groups())
    return partial(f, a, b)


def run(lines, w=SCREEN_W, h=SCREEN_H):
    screen = np.zeros((h, w))
    for line in lines:
        op = get_instruction(line)
        screen = op(screen)
    return screen


def count_pixels(lines):
    return run(lines).sum()


def print_screen(lines, w=SCREEN_W, h=SCREEN_H):
    screen = run(lines, w, h)
    for line in screen:
        print("".join(map(lambda i: "#" if i else " ", line)))


def main(data: str):
    lines = data.splitlines()
    yield count_pixels(lines)
    yield print_screen(lines)
