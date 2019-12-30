import numpy as np

from libaoc import BaseRunner
from libaoc.matrix import convolve_2d_3x3, load_string_matrix

WEIGHTS = 2 ** np.arange(25)
FILTER = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
EMPTY = np.zeros((5, 5), dtype=int)

OUTER_MASK = np.pad(np.zeros((3, 3), dtype=int), 1, constant_values=1)
INNER_MASK = EMPTY.copy()
INNER_MASK[[2, 1, 2, 3], [1, 2, 3, 2]] = 1


def load_bugs(data: str):
    return (load_string_matrix(data) == "#") * 1


def step(bugs):
    neighbors = convolve_2d_3x3(bugs, FILTER)
    one_adj, two_adj = neighbors == 1, neighbors == 2
    bugs_alive = bugs & one_adj
    infected = (~bugs) & (one_adj | two_adj)
    return bugs_alive | infected


def biodiversity(bugs):
    return np.sum(bugs.reshape((25,)) * WEIGHTS)


def first_repeat(bugs):
    visited = set()
    while (score := biodiversity(bugs)) not in visited:
        visited.add(score)
        bugs = step(bugs)
    return score


def recursive_step(bugs, inner=None, outer=None):
    neighbors = convolve_2d_3x3(bugs, FILTER)

    if inner is not None:
        neighbors[1, 2] += np.sum(inner[0, :])
        neighbors[2, 1] += np.sum(inner[:, 0])
        neighbors[3, 2] += np.sum(inner[4, :])
        neighbors[2, 3] += np.sum(inner[:, 4])

    if outer is not None:
        neighbors[0, :] += outer[1, 2]
        neighbors[:, 0] += outer[2, 1]
        neighbors[4, :] += outer[3, 2]
        neighbors[:, 4] += outer[2, 3]

    one_adj, two_adj = neighbors == 1, neighbors == 2
    bugs_alive = bugs & one_adj
    infected = (~bugs) & (one_adj | two_adj)
    bugs = bugs_alive | infected
    bugs[2, 2] = 0
    return bugs * 1


def recursive_step_all(bug_layers):
    new_layers = {}
    for i, bugs in bug_layers.items():
        new_layers[i] = recursive_step(
            bugs, bug_layers.get(i + 1), bug_layers.get(i - 1)
        )
    max_i, min_i = max(bug_layers), min(bug_layers)
    if np.any(bug_layers[max_i] & INNER_MASK):
        new_layers[max_i + 1] = recursive_step(EMPTY, outer=bug_layers[max_i])
    if np.any(bug_layers[min_i] & OUTER_MASK):
        new_layers[min_i - 1] = recursive_step(EMPTY, inner=bug_layers[min_i])
    return new_layers


def count_after_n_steps(start_bugs, steps):
    layers = {0: start_bugs}
    for _ in range(steps):
        layers = recursive_step_all(layers)
    return sum(np.sum(bugs) for bugs in layers.values())


class AocRunner(BaseRunner):
    year = 2019
    day = 24

    def run(self, data):
        bugs = load_bugs(data)
        yield first_repeat(bugs)
        yield count_after_n_steps(bugs, steps=200)
