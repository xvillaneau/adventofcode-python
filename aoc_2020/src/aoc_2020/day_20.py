from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from math import prod
import re

from more_itertools import split_at
import numpy as np
from scipy.signal import convolve


# Hard-coded table for reversing 5-bit values
# Using this is A LOT faster than reversing bit by bit.
REVERSED = [
    0x00, 0x10, 0x08, 0x18, 0x04, 0x14, 0x0c, 0x1c,
    0x02, 0x12, 0x0a, 0x1a, 0x06, 0x16, 0x0e, 0x1e,
    0x01, 0x11, 0x09, 0x19, 0x05, 0x15, 0x0d, 0x1d,
    0x03, 0x13, 0x0b, 0x1b, 0x07, 0x17, 0x0f, 0x1f,
]
FACTORS = 2 ** (np.arange(10, 0, -1) - 1)


def reverse_bits(num: int) -> int:
    return (REVERSED[num & 0x1f] << 5) + REVERSED[num >> 5]


def border_id(border) -> int:
    id = sum(border * FACTORS)
    return min(id, reverse_bits(id))


def configurations(matrix):
    for _ in range(2):
        for _ in range(4):
            yield matrix
            matrix = np.rot90(matrix)
        matrix = np.flip(matrix, axis=0)


@dataclass
class TileData:
    id: int
    tile: np.ndarray

    # Neighbor IDs, 0 = none
    top: int = 0
    left: int = 0
    bottom: int = 0
    right: int = 0

    @classmethod
    def parse(cls, data: list[str]):
        tile_id, *tile = data
        tile_id = int(re.search(r'\d+', tile_id).group())
        tile = np.array([list(row) for row in tile]) == '#'
        return cls(tile_id, tile)

    def add_link(self, side: int, neighbor: int):
        top, left, bottom, right = self.sides
        if side == top:
            self.top = neighbor
        elif side == left:
            self.left = neighbor
        elif side == right:
            self.right = neighbor
        elif side == bottom:
            self.bottom = neighbor
        else:
            raise IndexError(f"Tile {self.id} has no side {side}")

    def transform_for(self, top: int, left: int):
        # Rotate and flip the tile until it matches two neighbors
        if top in (self.left, self.right):
            self.rot90()
        if top == self.bottom:
            self.flip_y()
        if left == self.right:
            self.flip_x()

    def flip_x(self):
        self.tile = np.flip(self.tile, axis=1)
        self.left, self.right = self.right, self.left

    def flip_y(self):
        self.tile = np.flip(self.tile, axis=0)
        self.top, self.bottom = self.bottom, self.top

    def rot90(self):
        self.tile = np.rot90(self.tile)
        top, lft, bot, rgt = self.neighbors
        self.top, self.left, self.bottom, self.right = rgt, top, lft, bot

    @cached_property
    def sides(self):
        # Note: cached for performance, but no longer correct after the
        # tile gets transformed. We only use it before that thankfully.
        top = border_id(self.tile[0])
        bottom = border_id(self.tile[-1])
        left = border_id(self.tile[:, 0])
        right = border_id(self.tile[:, -1])
        return top, left, bottom, right

    @property
    def neighbors(self):
        return self.top, self.left, self.bottom, self.right

    @property
    def is_corner(self):
        return self.neighbors.count(0) == 2

    def get_data(self):
        return self.tile[1:-1, 1:-1]


def parse_tiles(data: list[str]):
    tiles: dict[int, TileData] = {}
    links: dict[int, set[int]] = defaultdict(set)

    # Step 1: parse every tile, and build mapping of border IDs
    for raw_tile in split_at(data, lambda line: len(line) == 0):
        tile = TileData.parse(raw_tile)
        tiles[tile.id] = tile

        for side in tile.sides:
            links[side].add(tile.id)

    # Step 2: go through pairs of tiles with common border IDs, and mark
    #         them as neighbors of each other.
    for link, linked in links.items():
        if len(linked) > 2:
            raise ValueError("Can't solve this")
        elif len(linked) < 2:
            # Border is on a side of the full image
            continue

        tile_a, tile_b = linked
        tiles[tile_a].add_link(link, tile_b)
        tiles[tile_b].add_link(link, tile_a)

    return tiles


def assemble_tiles(tiles: dict[int, TileData]):
    # Start at any corner
    tile_id = next(id for id, tile in tiles.items() if tile.is_corner)

    # Go over the full image row by row
    tile_map = []
    while tile_id != 0:

        row = []
        while tile_id != 0:
            # Transform the tile to match its bottom and top neighbors
            top = tile_map[-1][len(row)].id if tile_map else 0
            left = row[-1].id if row else 0
            tile = tiles[tile_id]
            tile.transform_for(top, left)

            # Continue with its right neighbor
            row.append(tile)
            tile_id = tile.right

        # End of row if right neighbor is 0, continue to next row
        tile_map.append(row)
        tile_id = row[0].bottom

    blocks = [[tile.get_data() for tile in row] for row in tile_map]
    return np.block(blocks)


MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]
MONSTER = 1 * (np.array([list(ln) for ln in MONSTER]) == '#')


def water_roughness(data):
    detected = np.sum(MONSTER)
    for monster in configurations(MONSTER):
        matches = convolve(data, monster)
        if (found := np.sum(matches == detected)) > 0:
            return np.sum(data) - found * detected
    raise ValueError("Monster not found!")


def main(data: str):
    tiles = parse_tiles(data.splitlines())
    yield prod(id for id, tile in tiles.items() if tile.is_corner)

    assembled = assemble_tiles(tiles)
    yield water_roughness(assembled)
