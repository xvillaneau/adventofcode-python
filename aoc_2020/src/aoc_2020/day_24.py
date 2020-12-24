from collections import defaultdict
from collections.abc import Iterator

from more_itertools import unzip
import numpy as np
from scipy.signal import convolve

from libaoc.vectors import Vect2D, UP, LEFT, DOWN, RIGHT, ORIGIN

EAST = RIGHT
NORTH_EAST = UP + RIGHT
NORTH_WEST = UP
WEST = LEFT
SOUTH_WEST = DOWN + LEFT
SOUTH_EAST = DOWN

VECTORS = {
    'e': EAST,
    'ne': NORTH_EAST,
    'nw': NORTH_WEST,
    'w': WEST,
    'se': SOUTH_EAST,
    'sw': SOUTH_WEST,

}

FILTER = np.array([[1, 1, 0], [1, 0, 1], [0, 1, 1]], dtype=int)


def parse_vectors(line: str) -> Iterator[Vect2D]:
    ns = ''
    for c in line:
        if c in 'ns':
            ns = c
        elif ns:
            yield VECTORS[ns + c]
            ns = ''
        else:
            yield VECTORS[c]


def map_tiles(tiles: list[str]):
    flipped: dict[Vect2D, bool] = defaultdict(bool)
    for tile in tiles:
        pos = sum(parse_vectors(tile), start=ORIGIN)
        flipped[pos] ^= True

    black_tiles = {pos for pos, flip in flipped.items() if flip}
    xs, ys = map(list, unzip(black_tiles))
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    floor = np.zeros((max_x - min_x + 1, max_y - min_y + 1), dtype=int)
    coordinates = np.array([(x - min_x, y - min_y) for x, y in black_tiles])
    floor[coordinates[:, 0], coordinates[:, 1]] = 1

    return floor


def flip_tiles(tiles):
    counts = convolve(tiles, FILTER)
    stay_black = (counts == 1) & np.pad(tiles, 1)
    new_blacks = (counts == 2)
    return stay_black | new_blacks


def day_100(tiles):
    for _ in range(100):
        tiles = flip_tiles(tiles)
    return tiles


def main(data: str):
    tiles = map_tiles(data.splitlines())
    yield np.sum(tiles)
    yield np.sum(day_100(tiles))
