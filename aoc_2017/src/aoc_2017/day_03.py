import math
from typing import Tuple, Set

Pos = Tuple[int, int]


def position(address: int) -> Pos:
    """Get the coordinates of an address"""
    if address == 1:
        return 0, 0
    layer = (int(math.sqrt(address - 1)) + 1) // 2
    side_length = 2 * layer
    layer_start = (2 * layer - 1) ** 2
    side, side_pos = divmod(address - layer_start, side_length)
    vectors = [(layer, side_pos - layer), (layer - side_pos, layer),
               (-layer, layer - side_pos), (side_pos - layer, -layer)]
    return vectors[side % 4]


def neighbors(address: int) -> Set[Pos]:
    """Get the positions of all neighbors of an address"""
    x, y = position(address)
    box = (-1, 0, 1)
    return set((x + i, y + j) for i in box for j in box) - {(x, y)}


def n_steps(address: int) -> int:
    """Calculate how many steps are needed to reach an address"""
    x, y = position(address)
    return abs(x) + abs(y)


def spiral_neighbors():
    """Generator that yields a spiral progression"""
    mem = {(0, 0): 1}
    address = 1
    yield 1

    while True:
        address += 1
        head = sum(mem.get(pos, 0) for pos in neighbors(address))
        mem[position(address)] = head
        yield head


def part_2(num: int):
    spiral = spiral_neighbors()
    return next(i for i in spiral if i > num)


if __name__ == '__main__':
    from libaoc import static_input, simple_main
    simple_main(2017, 3, static_input(368078), n_steps, part_2)
