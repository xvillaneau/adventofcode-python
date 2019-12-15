from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Body:
    name: str
    satellites: List['Body'] = field(default_factory=list)
    center: Optional['Body'] = None

    def parents(self):
        res, p = [], self.center
        while p:
            res.append(p)
            p = p.center
        return res

    def orbits(self, depth=1):
        return (
            sum(sat.orbits(depth+1) for sat in self.satellites)
            + len(self.satellites) * depth
        )


def parse_map(orbits_map: List[str]):
    bodies: Dict[str, Body] = {}
    for line in orbits_map:
        left, right = line.split(')')
        sun = bodies.setdefault(left, Body(left))
        planet = bodies.setdefault(right, Body(right))
        planet.center = sun
        sun.satellites.append(planet)
    return bodies


def part_1(orbits_map: List[str]):
    bodies = parse_map(orbits_map)
    return bodies['COM'].orbits()


def part_2(orbits_map: List[str]):
    bodies = parse_map(orbits_map)
    from_you, from_san = bodies["YOU"].parents(), bodies["SAN"].parents()
    from_you.reverse()
    from_san.reverse()
    fork = next(i for i, (a, b) in enumerate(zip(from_san, from_you)) if a != b)
    return len(from_you) + len(from_san) - 2 * fork


if __name__ == '__main__':
    from libaoc import simple_main, files
    simple_main(2019, 6, files.read_lines, part_1, part_2)
