import numpy as np

from libaoc.matrix import load_string_matrix, convolve_2d

OPEN, TREES, LUMBERYARD = 0, 1, 2


def parse_input(data: str):
    str_mat = load_string_matrix(data)
    area = np.zeros(str_mat.shape, dtype=int)
    area += np.where(str_mat == "|", TREES, OPEN)
    area += np.where(str_mat == "#", LUMBERYARD, OPEN)
    return area


def repr_area(area):
    str_mat = np.choose(area, ".|#")
    return "\n".join("".join(line) for line in str_mat)


def print_area(area):
    print(repr_area(area))


def hash_area(area):
    return hash(tuple(np.ravel(area)))


ADJACENT = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def transform(area):
    open_ = area == OPEN
    trees = area == TREES
    yards = area == LUMBERYARD

    adj_trees = convolve_2d(trees, ADJACENT)
    adj_yards = convolve_2d(yards, ADJACENT)

    area = np.where(open_ & (adj_trees >= 3), TREES, area)
    area = np.where(trees & (adj_yards >= 3), LUMBERYARD, area)
    area = np.where(yards & (adj_yards * adj_trees == 0), OPEN, area)
    return area


def value_after(area, minutes):
    step, visited = 0, {}
    while step < minutes:
        if (area_hash := hash_area(area)) in visited:
            period = step - visited[area_hash]
            step += ((minutes - step) // period) * period
            break
        visited[area_hash] = step
        area = transform(area)
        step += 1
    for _ in range(step, minutes):
        area = transform(area)
    return np.sum(area == TREES) * np.sum(area == LUMBERYARD)


def main(data: str):
    area = parse_input(data)
    yield value_after(area, 10)
    yield value_after(area, 1_000_000_000)
