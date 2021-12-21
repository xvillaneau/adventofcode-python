from collections import defaultdict
from itertools import product, combinations

import numpy as np

from libaoc.parsers import parse_integer_table


def _rotations():
    def _rot_4(mat, rot):
        for _ in range(4):
            yield mat
            mat = mat @ rot

    yield from _rot_4(ID, ROT_X)
    yield from _rot_4(ROT_Y @ ROT_Y, ROT_X)
    yield from _rot_4(ROT_Y, ROT_Z)
    yield from _rot_4(ROT_Y.transpose(), ROT_Z)
    yield from _rot_4(ROT_Z, ROT_Y)
    yield from _rot_4(ROT_Z.transpose(), ROT_Y)


ID = np.identity(3, dtype=int)
ROT_X = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype=int)
ROT_Y = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]], dtype=int)
ROT_Z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=int)
ROTATIONS = list(_rotations())


def parse_data(data: str) -> list[np.ndarray]:
    scanners = data.strip().split("\n\n")
    points = []
    for scan_data in scanners:
        _, _, scan_points = scan_data.partition("\n")
        points.append(parse_integer_table(scan_points, delimiter=","))
    return points


def detect_overlap(points_a: np.ndarray, points_b: np.ndarray):
    for rot in ROTATIONS:
        rot_b = points_b @ rot

        deltas = defaultdict(int)
        for a, b in product(points_a, rot_b):
            delta = tuple(a - b)
            deltas[delta] += 1
            if deltas[delta] == 12:
                return a - b, rot
        else:
            continue

    return None


def locate_scanners(scans: list[np.ndarray]):
    placed: dict[int, tuple[np.ndarray, np.ndarray]] = {
        0: (np.array([0, 0, 0]), ID)
    }
    to_place: list[int] = list(range(1, len(scans)))
    no_overlap: set[frozenset[int]] = set()

    while to_place:
        scan = to_place.pop(0)
        points_a = scans[scan]

        for target in placed:
            pair = frozenset((scan, target))
            if pair in no_overlap:
                continue
            print("Matching", scan, "and", target)

            points_b = scans[target]
            match = detect_overlap(points_b, points_a)
            if match is None:
                print("No match!")
                no_overlap.add(pair)
                continue

            rel_mov, rel_rot = match
            ref_mov, ref_rot = placed[target]
            placed[scan] = (ref_mov + rel_mov @ ref_rot, rel_rot @ ref_rot)
            break
        else:
            to_place.append(scan)

    return placed


def reduce_points(scans: list[np.ndarray], scanners):
    all_points = set()
    for i, points in enumerate(scans):
        mov, rot = scanners[i]
        all_points.update(tuple(pt) for pt in mov + points @ rot)
    return all_points


def longest_distance(scanners):
    def distances():
        vectors = (mov for mov, _ in scanners.values())
        for a, b in combinations(vectors, 2):
            x, y, z = a - b
            yield abs(x) + abs(y) + abs(z)
    return max(distances())


def main(data: str):
    scans = parse_data(data)
    scanners = locate_scanners(scans)
    yield len(reduce_points(scans, scanners))
    yield longest_distance(scanners)
