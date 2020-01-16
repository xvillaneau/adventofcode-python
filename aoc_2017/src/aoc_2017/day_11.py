import math
from typing import Dict, List, Tuple
import numpy as np

HEX_V = .5
HEX_H = math.sqrt(3) / 2

DIRS = {
    "n": np.array([0, 1.]),
    "s": np.array([0, -1.]),
    "ne": np.array([HEX_H, HEX_V]),
    "se": np.array([HEX_H, -HEX_V]),
    "sw": np.array([-HEX_H, -HEX_V]),
    "nw": np.array([-HEX_H, HEX_V]),
}


def group_instructions(instructions: List[str]) -> np.ndarray:
    vectors = np.array([DIRS[i] for i in instructions])
    return vectors.sum(axis=0)


def dominant_directions(vector: np.ndarray) -> Tuple[str, str]:

    def _dir_prod(dir_name):
        return vector.dot(DIRS[dir_name])

    dirs = set(DIRS.keys())
    d1 = max(dirs, key=_dir_prod)
    d2 = max(dirs - {d1}, key=_dir_prod)
    return d1, d2


def decompose(vector: np.ndarray) -> Dict[str, float]:
    d1, d2 = dominant_directions(vector)
    base_mat = np.linalg.inv([DIRS[d1], DIRS[d2]])
    v1, v2 = vector.dot(base_mat)
    return {d1: v1, d2: v2}


def distance(vector: np.ndarray) -> float:
    dirs = decompose(vector)
    return sum(dirs.values())


def max_distance(instructions: List[str]) -> float:
    vectors = np.array([DIRS[i] for i in instructions])
    locations = vectors.cumsum(axis=0)
    return max(distance(v) for v in locations)


def main(data: str):
    lost_path = data.strip().split(",")
    lost_loc = group_instructions(lost_path)
    yield int(round(distance(lost_loc)))
    yield int(round(max_distance(lost_path)))
