import numpy as np
from scipy.ndimage import label
from scipy.signal import argrelmin


def load_map(data: str):
    return np.array(
        [list(map(int, line)) for line in data.strip().splitlines()],
        dtype=int,
    )


def find_minima(heightmap: np.ndarray):
    ext_map = np.pad(heightmap, ((1, 1),), 'constant', constant_values=9)
    min_0 = set(zip(*argrelmin(ext_map, axis=0)))
    min_1 = set(zip(*argrelmin(ext_map, axis=1)))
    return [(x - 1, y - 1) for x, y in min_0 & min_1]


def risk_level(heightmap: np.ndarray) -> int:
    minima = find_minima(heightmap)
    return sum(1 + heightmap[x, y] for x, y in minima)


def find_basins(heightmap: np.ndarray) -> int:
    basins, n_basins = label(heightmap < 9)
    sizes = sorted(np.sum(basins == n + 1) for n in range(n_basins))
    return sizes[-3] * sizes[-2] * sizes[-1]


def main(data: str):
    heightmap = load_map(data)
    yield risk_level(heightmap)
    yield find_basins(heightmap)
