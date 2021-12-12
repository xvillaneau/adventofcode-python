import numpy as np
from scipy.signal import convolve

from libaoc.parsers import parse_digit_matrix

FLASH_FILTER = parse_digit_matrix("""
111
101
111
""")

def octopus_step(levels: np.ndarray) -> tuple[np.ndarray, int]:
    flashes = np.zeros(levels.shape, int)
    levels = np.copy(levels)
    levels += 1
    while np.any(step_flashes := levels > 9):
        flash_energy = convolve(step_flashes, FLASH_FILTER, mode="same")
        levels += flash_energy
        flashes |= step_flashes
        levels = np.where(flashes, 0, levels)
    # noinspection PyTypeChecker
    return levels, np.sum(flashes, dtype=int)


def count_flashes(levels: np.ndarray, steps: int) -> int:
    flashes = 0
    for i in range(steps):
        levels, n = octopus_step(levels)
        flashes += n
    return flashes


def detect_sync(levels: np.ndarray) -> int:
    i = 0
    while not np.all(levels == 0):
        i += 1
        levels, _ = octopus_step(levels)
    return i


def main(data: str):
    levels = parse_digit_matrix(data)
    yield count_flashes(levels, 100)
    yield detect_sync(levels)
