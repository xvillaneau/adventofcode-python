from typing import List
import numpy as np
from libaoc import simple_main, files


def triangle_possible(sides: List[int]):
    s1, s2, lg = sorted(sides)
    return s1 + s2 > lg


def count_possible(triangles):
    return sum(map(triangle_possible, triangles))


def count_transpose(triangles):
    x, _ = triangles.shape
    new_triangles = np.hstack(np.vsplit(triangles, x // 3)).transpose()
    return count_possible(new_triangles)


if __name__ == '__main__':
    simple_main(2016, 3, files.read_int_table, count_possible, count_transpose)
