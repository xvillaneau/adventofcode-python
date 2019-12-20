from collections.abc import Iterator
from itertools import count

import numpy as np

from libaoc.vectors import Vect2D, UP, RIGHT, ORIGIN
from aoc_2019.intcode import read_program, CodeRunner


class DroneController:
    def __init__(self, runner):
        self._orig_runner = runner.copy()
        self.runner = runner.copy()
        self._explored = {}

    def __getitem__(self, item):
        x, y = item
        if (x, y) in self._explored:
            return self._explored[(x, y)]

        self.runner.send(x)
        self.runner.send(y)
        result = bool(next(self.runner))

        self.runner = self._orig_runner.copy()
        self._explored[(x, y)] = result
        return result


def scan_iter():
    for i in count(2):
        for j in range(i + 1):
            yield j, i - j


class EdgeWalker(Iterator):
    def __init__(self, controller: DroneController, invert=False):
        self.controller = controller
        self.u, self.v = (RIGHT, UP) if invert else (UP, RIGHT)
        self.pos = ORIGIN
        self._initial = True

    def __next__(self):
        if self._initial:
            self._initial = False
            return ORIGIN

        u, v = self.u, self.v
        for vector in (u, u + v, v):
            if self.controller[self.pos + vector]:
                self.pos += vector
                return self.pos

        # We've lost the edge !
        for i, j in scan_iter():
            vector = i * u + j * v
            if self.controller[self.pos + vector]:
                self.pos += vector
                return self.pos


def edge_matrix(controller: DroneController, invert=False, size=50):
    edge_mat = np.zeros((size, size), dtype=bool)

    for drone in EdgeWalker(controller, invert):
        x, y = ~drone if invert else drone
        if x >= size or y >= size:
            if x < size:
                edge_mat[x:, :] = True
            return edge_mat
        edge_mat[x, :y + 1] = True


def detect_ray_surface(controller: DroneController, size=50):
    top_edge = edge_matrix(controller, size=size).transpose()
    low_edge = edge_matrix(controller, invert=True, size=size)
    return np.sum(top_edge & low_edge)


def locate_square(controller: DroneController, size=100):
    top_edge = EdgeWalker(controller)
    low_edge = EdgeWalker(controller, invert=True)

    square_vect = Vect2D(size - 1, 1 - size)

    top, low = next(top_edge), next(low_edge)
    while (ref := top + square_vect) != low:
        if abs(ref) > abs(low):
            low = next(low_edge)
        else:
            top = next(top_edge)
    return top + Vect2D(0, 1 - size)


def day_19(code):
    controller = DroneController(CodeRunner(code))
    yield detect_ray_surface(controller)
    x, y = locate_square(controller)
    print(x, y)
    yield x * 10_000 + y


if __name__ == '__main__':
    from libaoc import iter_main
    iter_main(2019, 19, read_program, day_19)
