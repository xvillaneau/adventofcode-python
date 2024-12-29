from itertools import count, combinations
import numpy as np

from libaoc.matrix import load_string_matrix
from libaoc.vectors import Vect2D

Dims = tuple[int, int]
Antenna = tuple[str, Vect2D]


def parse_input(data: str) -> tuple[Dims, list[Antenna]]:
    mat = load_string_matrix(data)
    coords = np.argwhere(mat != ".")

    antennas = []
    for x, y in coords:
        antennas.append((mat[x, y], Vect2D(x, y)))

    return mat.shape, antennas


def in_map(dims: Dims, p: Vect2D):
    mx, my = dims
    return 0 <= p.x < mx and 0 <= p.y < my


def list_aligned(a: Vect2D, b: Vect2D, harmonic=False):
    d = b - a
    if not harmonic:
        yield b + d
        return
    for n in count():
        yield b + d * n


def list_antinodes(dims, nodes: list[Vect2D], harmonic=False):
    for a, b in combinations(nodes, 2):
        for n in list_aligned(a, b, harmonic):
            if not in_map(dims, n):
                break
            yield n
        for n in list_aligned(b, a, harmonic):
            if not in_map(dims, n):
                break
            yield n


def list_all_antinodes(dims: Dims, antennas: list[Antenna], harmonic=False):
    by_freq: dict[str, list[Vect2D]] = {}
    for freq, pos in antennas:
        if freq not in by_freq:
            by_freq[freq] = [pos]
        else:
            by_freq[freq].append(pos)

    for freq, nodes in by_freq.items():
        for p in list_antinodes(dims, nodes, harmonic):
            yield freq, p


def part_1(dims, antennas):
    antinodes = {p for _, p in list_all_antinodes(dims, antennas)}
    return len(antinodes)


def part_2(dims, antennas):
    antinodes = {p for _, p in list_all_antinodes(dims, antennas, harmonic=True)}
    return len(antinodes)


def main(data: str):
    dims, antennas = parse_input(data)
    yield part_1(dims, antennas)
    yield part_2(dims, antennas)
