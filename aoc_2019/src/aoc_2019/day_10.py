from cmath import phase
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations, islice
from math import pi
from typing import Dict, FrozenSet, Set, NamedTuple

from libaoc import BaseRunner
from libaoc.primes import gcd
from libaoc.vectors import Vect2D


@dataclass(frozen=True)
class Pt(Vect2D):
    def angle(self):
        if self.x == 0 and self.y < 0:
            return 0.0
        return phase(complex(self) * -1j) + pi

    def __lt__(self, other):
        if not isinstance(other, Pt):
            return NotImplemented
        return (self.angle()) < other.angle()

    def __eq__(self, other):
        return super().__eq__(other)


def min_fraction(vector: Pt) -> Pt:
    if vector == (0, 0):
        return vector
    return vector // gcd(*vector)


class Field(NamedTuple):
    asteroids: Set[Pt]
    size_x: int
    size_y: int

    @classmethod
    def from_map(cls, space_map: str):
        asteroids = set()
        rows = space_map.strip().splitlines()
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                if char == '#':
                    asteroids.add(Pt(x, y))
        return Field(asteroids, len(rows[0]), len(rows))

    def in_bounds(self, point: Pt):
        return 0 <= point.x < self.size_x and 0 <= point.y < self.size_y

    def iter_sight(self, start: Pt, target: Pt):
        unit = min_fraction(target - start)
        pos = start + unit
        while self.in_bounds(pos):
            if pos in self.asteroids:
                yield pos
            pos += unit


def analyze_asteroids(field: Field):
    lines_of_sight: Dict[Pt, Set[Pt]] = defaultdict(set)
    explored: Set[FrozenSet[Pt, Pt]] = set()

    for pt_a, pt_b in combinations(field.asteroids, 2):
        if frozenset((pt_a, pt_b)) in explored:
            continue
        behind = [pt_a]
        for point in field.iter_sight(pt_a, pt_b):
            prev = behind[-1]
            lines_of_sight[point].add(prev)
            lines_of_sight[prev].add(point)
            explored.add(frozenset((prev, point)))
            for prev in behind[:-1]:
                explored.add(frozenset((prev, point)))
            behind.append(point)
    return lines_of_sight


def exterminate(field: Field, station_sight: Set[Pt], station: Pt):
    asteroids = field.asteroids.copy()
    station_sight = station_sight.copy()

    def sort_by_angle(_asteroids):
        return list(sorted(_asteroids, key=lambda pt: pt - station, reverse=True))

    current_sight = []
    while station_sight:
        if not current_sight:
            current_sight = sort_by_angle(station_sight)
        vaporized = current_sight.pop()
        yield vaporized
        asteroids.remove(vaporized)
        station_sight.remove(vaporized)
        if point := next(field.iter_sight(station, vaporized), None):
            station_sight.add(point)


def find_station(sight_scores):
    return max(sight_scores, key=lambda pt: len(sight_scores[pt]))


class AocRunner(BaseRunner):
    year = 2019
    day = 10

    def run(self, space_map: str):
        field = Field.from_map(space_map)
        sight_scores = analyze_asteroids(field)
        station = find_station(sight_scores)
        yield len(sight_scores[station])
        vaporize_iter = exterminate(field, sight_scores[station], station)
        _vap = next(islice(vaporize_iter, 199, None))
        yield _vap.x * 100 + _vap.y
