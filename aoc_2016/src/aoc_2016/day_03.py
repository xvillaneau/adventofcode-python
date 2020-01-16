from typing import List
import numpy as np

from libaoc.parsers import parse_integer_table


def triangle_possible(sides: List[int]):
    s1, s2, lg = sorted(sides)
    return s1 + s2 > lg


def count_possible(triangles):
    return sum(map(triangle_possible, triangles))


def count_transpose(triangles):
    x, _ = triangles.shape
    new_triangles = np.hstack(np.vsplit(triangles, x // 3)).transpose()
    return count_possible(new_triangles)


def main(data: str):
    triangles = parse_integer_table(data)
    yield count_possible(triangles)
    yield count_transpose(triangles)
