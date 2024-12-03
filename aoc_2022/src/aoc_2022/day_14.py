import numpy as np
from more_itertools import windowed
from more_itertools.more import minmax

from libaoc.vectors import Vect2D


class Cave:
    def __init__(self, rocks: list[list[Vect2D]]):
        self.x_min, self.x_max = minmax(p.x for r in rocks for p in r)
        self.y_max = max(p.y for r in rocks for p in r)
        self.x_offset = self.x_min - self.y_max

        self.sand = 0

        width = self.x_max - self.x_min + self.y_max * 2
        depth = self.y_max + 2
        self.cave = np.zeros((width, depth), dtype=int)

        for rock in rocks:
            for start, end in windowed(rock, 2):
                diff = end - start
                unit = diff // abs(diff)
                pos = start
                while pos != end:
                    self[pos.x, pos.y] = 1
                    pos += unit
                self[end.x, end.y] = 1

        self[500, 0] = -1  # Start point

    def __setitem__(self, key: tuple[int, int], value):
        x, y = key
        self.cave[x - self.x_offset, y] = value

    def __getitem__(self, item: tuple[int, int]):
        x, y = item
        return self.cave[x - self.x_offset, y]

    def fall_sand(self, part_2=False):
        x, y = 500, 0

        if self[x, y] > 0:
            return False

        while 1:
            col = self.cave[x - self.x_offset, y:]
            if col[0] > 0:
                raise ValueError("ran into solid!")
            if np.all(col <= 0):
                if part_2:
                    y = self.y_max + 1
                    self[x, y] = 2
                    self.sand += 1
                    return True
                else:
                    return False
            else:
                y = int(np.argmax(col > 0)) + y - 1

            # Check down left
            if self[x-1, y+1] <= 0:
                x = x-1
                y = y+1
                continue
            # Check down right
            if self[x+1, y+1] <= 0:
                x = x+1
                y = y+1
                continue

            # We're stuck
            self[x, y] = 2
            self.sand += 1
            return True

        return False


    def print(self) -> str:
        symbols = "+.#o"
        out = ""
        for i in range(self.y_max + 2):
            row = self.cave[:, i]
            line = "".join(symbols[n+1] for n in row)
            out += line + "\n"
        return out

def parse_input(data: str):

    def parse_line(ln: str):
        points = []
        for pair in ln.split(" -> "):
            xs, _, ys = pair.partition(",")
            points.append(Vect2D(int(xs), int(ys)))
        return points

    return [parse_line(ln) for ln in data.strip().splitlines()]


def main(data: str):
    rocks = parse_input(data)
    cave = Cave(rocks)

    while cave.fall_sand():
        pass

    yield cave.sand

    # TODO: Part 2 works, but is really slow. Make diagonal propagation faster!
    while cave.fall_sand(part_2=True):
        pass

    yield cave.sand
