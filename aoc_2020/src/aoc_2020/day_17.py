import numpy as np
from scipy.signal import convolve

from libaoc.matrix import load_string_matrix


def parse_start(data: str, dims=3):
    start = load_string_matrix(data) == '#'
    return np.expand_dims(start, tuple(range(dims - 2)))


def step(layers):
    filter = np.ones((3,) * layers.ndim, dtype=int)
    counts = convolve(layers, filter) - np.pad(layers, 1)
    c2, c3 = counts == 2, counts == 3
    return c3 | (c2 & np.pad(layers, 1))


def boot_sequence(start):
    state = start
    for _ in range(6):
        state = step(state)
    return np.sum(state)


def main(data: str):
    yield boot_sequence(parse_start(data, dims=3))
    yield boot_sequence(parse_start(data, dims=4))
