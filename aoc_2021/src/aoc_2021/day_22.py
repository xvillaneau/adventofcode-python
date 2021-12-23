import math
import re
from dataclasses import dataclass
from functools import cached_property
from typing import Optional


RE_CUBOID = re.compile(
    r"""
    (on|off)
    \s
    x=(-?\d+)\.\.(-?\d+),
    y=(-?\d+)\.\.(-?\d+),
    z=(-?\d+)\.\.(-?\d+)
    """,
    re.VERBOSE
)


@dataclass
class Cuboid:
    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int
    val: int

    @classmethod
    def parse(cls, line: str):
        match = RE_CUBOID.fullmatch(line)
        on_off, *coords = match.groups()
        return Cuboid(*map(int, coords), 1 if on_off == "on" else 0)

    @property
    def in_init_area(self) -> bool:
        return all(-50 <= c <= 50 for c in self.tuple)

    @property
    def volume(self) -> int:
        sides = [
            (self.x1 - self.x0 + 1),
            (self.y1 - self.y0 + 1),
            (self.z1 - self.z0 + 1),
        ]
        return math.prod(sides)

    @cached_property
    def tuple(self):
        return self.x0, self.x1, self.y0, self.y1, self.z0, self.z1

    def __iter__(self):
        return iter(self.tuple)

    def __repr__(self):
        return (
            str(self.val)
            + f" x={self.x0}..{self.x1}"
            + f",y={self.y0}..{self.y1}"
            + f",z={self.z0}..{self.z1}"
        )

    def intersect(self, other: "Cuboid") -> Optional["Cuboid"]:
        if self.x1 < other.x0 or self.x0 > other.x1:
            return
        if self.y1 < other.y0 or self.y0 > other.y1:
            return
        if self.z1 < other.z0 or self.z0 > other.z1:
            return
        x0 = max(self.x0, other.x0)
        x1 = min(self.x1, other.x1)
        y0 = max(self.y0, other.y0)
        y1 = min(self.y1, other.y1)
        z0 = max(self.z0, other.z0)
        z1 = min(self.z1, other.z1)
        return Cuboid(x0, x1, y0, y1, z0, z1, -other.val)


def parse_data(data: str) -> list[Cuboid]:
    return [
        Cuboid.parse(ln)
        for ln in data.strip().splitlines()
    ]


def compute_overlap(cuboids: list[Cuboid], init=False):
    all_cuboids: list[Cuboid] = []
    for cub0 in cuboids:
        if init and not cub0.in_init_area:
            continue
        new_cuboids = [cub0]
        for cub1 in all_cuboids:
            if (intersect := cub0.intersect(cub1)) is not None:
                new_cuboids.append(intersect)
        all_cuboids.extend(new_cuboids)

    return sum(c.val * c.volume for c in all_cuboids)


def main(data: str):
    cuboids = parse_data(data)
    yield compute_overlap(cuboids, init=True)
    yield compute_overlap(cuboids, init=False)
