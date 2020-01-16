import numpy as np
from libaoc.parsers import parse_integer_table


def count_constellations(data: str):
    points = parse_integer_table(data, ",")

    n = points.shape[0]
    dims = (np.repeat(points[:, i][np.newaxis], n, axis=0) for i in range(4))
    links: np.ndarray = sum(abs(d - d.transpose()) for d in dims) <= 3

    constellations = 0
    buffer = []
    unassigned = set(range(n))

    while unassigned:
        if buffer:
            point = buffer.pop()
        else:
            constellations += 1
            point = unassigned.pop()

        next_points = set(np.nonzero(links[point])[0]) & unassigned
        unassigned -= next_points
        buffer.extend(next_points)

    return constellations


def main(data: str):
    yield count_constellations(data)
