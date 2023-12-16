import numpy as np
from libaoc.parsers import parse_digit_matrix


def map_visible_trees(trees: np.ndarray):
    def map_visible_1d(_trees, *transforms):
        for t in transforms:
            _trees = t(_trees)
        peaks = _trees[0]
        vis = np.zeros(_trees.shape, dtype=bool)
        vis[0] = np.ones(peaks.shape)
        for i, row in enumerate(_trees[1:], start=1):
            vis[i] = row > peaks
            peaks = np.fmax(peaks, row)
        for t in transforms[::-1]:
            vis = t(vis)
        return vis

    visible = np.zeros(trees.shape, dtype=int)
    visible += map_visible_1d(trees)
    visible += map_visible_1d(trees, np.flip)
    visible += map_visible_1d(trees, np.transpose)
    visible += map_visible_1d(trees, np.transpose, np.flip)
    return visible > 0


def main(data: str):
    trees = parse_digit_matrix(data)
    yield np.sum(map_visible_trees(trees))
