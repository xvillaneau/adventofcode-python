from dataclasses import dataclass
from itertools import combinations, count
import re
from typing import Iterable, List

from libaoc.math import merge_pulses


@dataclass(frozen=True)
class Vect3D:
    x: int
    y: int
    z: int

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __eq__(self, other):
        if isinstance(other, (Vect3D, tuple)):
            return tuple(self) == tuple(other)
        return False

    def __add__(self, other: "Vect3D"):
        return type(self)(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return self + -other

    def __neg__(self):
        return type(self)(-self.x, -self.y, -self.z)

    def __abs__(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


def compare(a: int, b: int):
    if a < b:
        return -1
    elif a > b:
        return 1
    return 0


@dataclass
class Moon:
    pos: Vect3D
    velocity: Vect3D = Vect3D(0, 0, 0)

    @property
    def energy(self):
        return abs(self.pos) * abs(self.velocity)


@dataclass
class Axis:
    positions: List[int]
    velocities: List[int]

    def __getitem__(self, item):
        return self.positions[item], self.velocities[item]

    def __len__(self):
        return len(self.positions)

    @property
    def state(self):
        return tuple(self.positions) + tuple(self.velocities)

    @classmethod
    def initial(cls, *positions: int):
        return cls(list(positions), [0] * len(positions))

    def run_step(self):
        for a, b in combinations(range(len(self)), 2):
            dv = compare(self.positions[a], self.positions[b])
            self.velocities[a] -= dv
            self.velocities[b] += dv
        for i, v in enumerate(self.velocities):
            self.positions[i] += v

    def find_repeat(self):
        explored = {self.state: 0}
        for i in count(1):
            self.run_step()
            if self.state in explored:
                start = explored[self.state]
                return start, i - start
            explored[self.state] = i


@dataclass
class System:
    x: Axis
    y: Axis
    z: Axis

    def __getitem__(self, item):
        x, vx = self.x[item]
        y, vy = self.y[item]
        z, vz = self.z[item]
        return Moon(Vect3D(x, y, z), Vect3D(vx, vy, vz))

    def __iter__(self) -> Iterable[Moon]:
        return iter(self[i] for i in range(len(self.x)))

    @property
    def energy(self):
        return sum(moon.energy for moon in self)

    @classmethod
    def from_input(cls, lines: List[str]):
        xs, ys, zs = [], [], []
        for line in lines:
            match = re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line)
            xs.append(int(match.group(1)))
            ys.append(int(match.group(2)))
            zs.append(int(match.group(3)))
        return cls(Axis.initial(*xs), Axis.initial(*ys), Axis.initial(*zs))

    def run_step(self):
        self.x.run_step()
        self.y.run_step()
        self.z.run_step()

    def simulate(self, steps: int):
        assert steps >= 0
        for _ in range(steps):
            self.run_step()

    def find_repeat(self):
        start, period = merge_pulses(
            self.x.find_repeat(), self.y.find_repeat(), self.z.find_repeat()
        )
        return start or period


def part_1(lines: List[str], steps=1000):
    system = System.from_input(lines)
    system.simulate(steps)
    return system.energy


def part_2(lines: List[str]):
    system = System.from_input(lines)
    return system.find_repeat()


def main(data: str):
    lines = data.splitlines()
    yield part_1(lines)
    yield part_2(lines)
