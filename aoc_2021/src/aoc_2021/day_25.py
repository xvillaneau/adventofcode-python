from itertools import count

import numpy as np
from scipy.signal import convolve2d

from libaoc.matrix import load_string_matrix

FILTER_R = np.array([[1, 0, 0]])
FILTER_D = FILTER_R.transpose()


def _sub_step(cucumbers: np.ndarray, char, filter, axis):
    can_move = convolve2d(cucumbers == ".", filter, "same", "wrap")
    moves = (cucumbers == char) & can_move
    moved = np.roll(moves, 1, axis=axis)
    cucumbers = np.where(moves, ".", cucumbers)
    return np.where(moved, char, cucumbers), np.any(moves)


def step(cucumbers: np.ndarray) -> tuple[np.ndarray, bool]:
    cucumbers, moved_r = _sub_step(cucumbers, ">", FILTER_R, 1)
    cucumbers, moved_d = _sub_step(cucumbers, "v", FILTER_D, 0)
    return cucumbers, moved_d or moved_r


def steps_to_static(cucumbers: np.ndarray) -> int:
    for steps in count(1):
        cucumbers, moved = step(cucumbers)
        if not moved:
            return steps


def main(data: str):
    cucumbers = load_string_matrix(data)
    yield steps_to_static(cucumbers)
