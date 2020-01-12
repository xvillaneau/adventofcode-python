import re
from typing import List, Tuple

import numpy as np

VOID, STREAM, WALL, WATER = 0, 1, 2, 3


def parse_input(data: str):
    segments = []
    re_num = re.compile(r"\d+")
    for line in data.splitlines():
        a, b0, b1 = map(int, re_num.findall(line))
        if line[0] == "x":
            segments.append((a, a, b0, b1))
        else:
            segments.append((b0, b1, a, a))
    return segments


def detect_borders(segments: List[Tuple[int, int, int, int]]):
    min_x = min(seg[0] for seg in segments) - 1
    max_x = max(seg[1] for seg in segments) + 1
    min_y = min(seg[2] for seg in segments)
    max_y = max(seg[3] for seg in segments)
    return min_x, max_x, min_y, max_y


def build_matrix(data):
    segments = parse_input(data)
    min_x, max_x, min_y, max_y = detect_borders(segments)
    mat = np.zeros((max_y - min_y + 1, max_x - min_x + 1), dtype=int)

    for seg in segments:
        x0, x1, y0, y1 = seg
        mat[y0 - min_y:y1 - min_y + 1, x0 - min_x:x1 - min_x + 1] = WALL

    return mat, min_x


def flow_down(matrix, x, y):
    next_down = np.nonzero(matrix[y:, x] > 1)[0]
    if next_down.any():
        lim = next_down.min()
        visited = matrix[y + lim - 1, x] == STREAM
        matrix[y:y + lim, x] = STREAM
        return [] if visited else [(1, x, y + lim - 1)]
    else:
        matrix[y:, x] = STREAM
        return []


def flow_sides(matrix, x, y):
    floor_view = np.sum(matrix[y:y + 2, :] > 1, axis=0)
    overflows = []

    # Look left
    left_walls = np.nonzero(floor_view[x - 1::-1] == WALL)[0]
    left_voids = np.nonzero(floor_view[x - 1::-1] == VOID)[0]
    if not len(left_walls) or np.min(left_voids) < np.min(left_walls):
        left_lim = x - np.min(left_voids) - 1
        overflows.append((0, left_lim, y))
    else:
        left_lim = x - np.min(left_walls)

    # Look right
    right_walls = np.nonzero(floor_view[x + 1:] == WALL)[0]
    right_voids = np.nonzero(floor_view[x + 1:] == VOID)[0]
    if not len(right_walls) or np.min(right_voids) < np.min(right_walls):
        right_lim = x + np.min(right_voids) + 1
        overflows.append((0, right_lim, y))
    else:
        right_lim = x + np.min(right_walls)

    if not overflows:
        matrix[y, left_lim:right_lim + 1] = WATER
        return [(1, x, y - 1)]

    matrix[y, left_lim:right_lim+1] = STREAM
    return overflows


def run_flows(matrix, start_offset):
    stack = [(0, 500 - start_offset, 0)]

    while stack:
        op, x, y = stack.pop()
        if op:
            stack.extend(flow_sides(matrix, x, y))
        else:
            stack.extend(flow_down(matrix, x, y))


def print_state(matrix):
    str_mat = np.choose(matrix, ".|#~")
    print("\n".join("".join(line) for line in str_mat))


def main(data: str):
    matrix, start_offset = build_matrix(data)
    run_flows(matrix, start_offset)
    yield np.sum(matrix & 1)
    yield np.sum(matrix == WATER)
