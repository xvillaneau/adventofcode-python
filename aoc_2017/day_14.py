from typing import List
import numpy as np

from aoc_2017.day_10 import int_hash

Row = List[bool]
Mem = List[Row]


def mem_row(mem_str: str, row_n: int) -> Row:
    row_int = int_hash(f'{mem_str}-{row_n}')
    row_bin = f'{row_int:0128b}'
    return [bit == '1' for bit in row_bin]


def count_bits(row: Row) -> int:
    return row.count(True)


def all_rows(mem_str: str) -> Mem:
    return [mem_row(mem_str, i) for i in range(128)]


def count_all_bits(rows: Mem) -> int:
    return sum(count_bits(row) for row in rows)


def num_regions(rows: Mem) -> int:
    # TODO: Fix me!
    label = lambda arr: (arr, None)
    regions, _ = label(np.array(rows))
    return regions.max()


def day_14(seed: str):
    puzzle = all_rows(seed)
    yield count_all_bits(puzzle)
    yield num_regions(puzzle)


if __name__ == '__main__':
    from libaoc import iter_main, static_input
    iter_main(2017, 14, static_input("amgozmfv"), day_14)
