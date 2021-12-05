import re

import numpy as np

Point = tuple[int, int]
Line = tuple[Point, Point]


def parse_data(data: str) -> list[Line]:
    lines = []
    for ln in data.splitlines():
        m = re.fullmatch(r"(\d+),(\d+) -> (\d+),(\d+)", ln)
        x1, y1, x2, y2 = map(int, m.groups())
        lines.append(((x1, y1), (x2, y2)))
    return lines


def make_matrix(lines: list[Line]) -> tuple[np.ndarray, Point]:
    x_min, y_min = x_max, y_max = lines[0][0]
    for (x1, y1), (x2, y2) in lines:
        x_min = min([x_min, x1, x2])
        x_max = max([x_max, x1, x2])
        y_min = min([y_min, y1, y2])
        y_max = max([y_max, y1, y2])

    dx, dy = x_max - x_min + 1, y_max - y_min + 1
    return np.zeros((dx, dy), dtype=int), (x_min, y_min)


def locate_vents(lines: list[Line]):
    field_hv, (xi, yi) = make_matrix(lines)
    field_dg = np.copy(field_hv)

    for (x1, y1), (x2, y2) in lines:
        x1, x2 = x1 - xi, x2 - xi
        y1, y2 = y1 - yi, y2 - yi

        if x1 == x2:
            y1, y2 = sorted([y1, y2])
            field_hv[x1, y1:y2+1] += 1
        elif y1 == y2:
            x1, x2 = sorted([x1, x2])
            field_hv[x1:x2+1, y1] += 1
        else:
            dx = 1 if x2 > x1 else -1
            dy = 1 if y2 > y1 else -1
            while x1 != x2:
                field_dg[x1, y1] += 1
                x1 += dx
                y1 += dy
            field_dg[x2, y2] += 1

    return field_hv, field_dg


def count_overlaps(field: np.ndarray):
    return np.sum(field > 1)


def main(data: str):
    lines = parse_data(data)
    field_hv, field_dg = locate_vents(lines)
    yield count_overlaps(field_hv)
    yield count_overlaps(field_hv + field_dg)
