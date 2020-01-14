from itertools import combinations

import numpy as np


def parse_input(data: str):
    nanobots = []
    for line in data.splitlines():
        pos_str, radius = line.split(">, r=")
        x, y, z = pos_str[5:].split(",")
        nanobots.append((int(x), int(y), int(z), int(radius)))
    return np.array(nanobots)


def range_of_strongest(nanobots):
    ind_strongest = np.argmax(nanobots[:, 3])
    rel_pos = nanobots[:, :3] - nanobots[ind_strongest, :3]
    distances = np.sum(abs(rel_pos), axis=1)
    return np.sum(distances <= nanobots[ind_strongest, 3])


def best_position(nanobots):
    n = nanobots.shape[0]
    x = np.repeat(nanobots[:, 0][np.newaxis], n, axis=0)
    y = np.repeat(nanobots[:, 1][np.newaxis], n, axis=0)
    z = np.repeat(nanobots[:, 2][np.newaxis], n, axis=0)
    r = np.repeat(nanobots[:, 3][np.newaxis], n, axis=0)

    dist = abs(x - x.transpose()) + abs(y - y.transpose()) + abs(z - z.transpose())
    intersect = dist <= (r + r.transpose())
    n_intersect = np.sum(intersect, axis=1)
    max_size = np.min(np.nonzero(np.sort(n_intersect)[::-1] <= np.arange(n)))

    distance = None
    for n_bots in range(max_size, 0, -1):
        indices = list(np.argwhere(n_intersect >= n_bots)[:, 0])
        for sub_indices in combinations(indices, n_bots):
            a = np.repeat([sub_indices], n_bots, axis=0)
            if not np.all(intersect[a, a.transpose()]):
                continue
            cluster = np.abs(nanobots[(sub_indices,)])
            cluster_dist = np.max(np.sum(cluster[:, :3], axis=1) - cluster[:, 3])
            if distance is None or cluster_dist < distance:
                distance = cluster_dist
        if distance is not None:
            return distance


def main(data: str):
    nanobots = parse_input(data)
    yield range_of_strongest(nanobots)
    yield best_position(nanobots)
