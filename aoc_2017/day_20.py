from collections import Counter
from itertools import combinations
from typing import Tuple, List

Vector = Tuple[float, float, float]


def vect_add(v1: Vector, v2: Vector) -> Vector:
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return x1 + x2, y1 + y2, z1 + z2


def vect_abs(vector: Vector) -> float:
    x, y, z = vector
    return abs(x) + abs(y) + abs(z)


class Particle(object):

    def __init__(self, position: Vector, velocity: Vector,
                 acceleration: Vector, index: int=-1):
        self.pos = position
        self.vit = velocity
        self.acc = acceleration
        self.index = index

    @classmethod
    def from_str_line(cls, line: str, line_no: int=-1) -> 'Particle':
        s_pos, s_vit, s_acc = line.split(', ')

        def _vec_from_str(string: str) -> Vector:
            coords = string[3:-1].strip()
            x, y, z = coords.split(',')
            return int(x), int(y), int(z)

        pos = _vec_from_str(s_pos)
        vit = _vec_from_str(s_vit)
        acc = _vec_from_str(s_acc)
        return cls(pos, vit, acc, line_no)

    def compute(self):
        self.vit = vect_add(self.vit, self.acc)
        self.pos = vect_add(self.pos, self.vit)

    def __eq__(self, other: 'Particle'):
        return self.pos == other.pos

    def __str__(self):
        return (f'{self.index}: '
                f'p=<{self.pos[0]},{self.pos[1]},{self.pos[2]}> '
                f'v=<{self.vit[0]},{self.vit[1]},{self.vit[2]}> '
                f'a=<{self.acc[0]},{self.acc[1]},{self.acc[2]}> ')


def read_file(lines: List[str]) -> List[Particle]:
    return [Particle.from_str_line(l, i) for i, l in enumerate(lines)]


def slowest(particles: List[Particle]) -> Particle:

    def _acc_abs(p: Particle) -> float:
        return vect_abs(p.acc)

    return min(particles, key=_acc_abs)


def divergent(particle_1: Particle, particle_2: Particle) -> bool:

    def _axis(p: Particle, n: int) -> Vector:
        return p.pos[n], p.vit[n], p.acc[n]

    def _axis_diverge(n: int):
        p0, v0, a0 = _axis(particle_1, n)
        p1, v1, a1 = _axis(particle_2, n)
        return ((a0 >= a1 and v0 >= v1 and p0 > p1)
                or (a0 <= a1 and v0 <= v1 and p0 < p1))

    return all(_axis_diverge(n) for n in (0, 1, 2))


def all_divergent(particles: List[Particle]) -> bool:
    return all(divergent(p1, p2) for p1, p2 in combinations(particles, 2))


def collision_engine(particles: List[Particle]) -> List[Particle]:

    parts = particles.copy()

    while not all_divergent(parts):

        pos_counts = Counter(p.pos for p in parts)
        collision_pos = set(pos for pos, n in pos_counts.items() if n != 1)
        parts = [p for p in parts if p.pos not in collision_pos]

        for p in particles:
            p.compute()

    return parts


def day_20(lines: List[str]):
    all_particles = read_file(lines)
    slow = slowest(all_particles)
    yield slow.index
    yield len(collision_engine(all_particles))


if __name__ == '__main__':
    from libaoc import iter_main, files
    iter_main(2017, 20, files.read_lines, day_20)
