from itertools import count
from operator import attrgetter
import re
from typing import NamedTuple, List

RE_DISC = re.compile(
    r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)."
)


class Disc(NamedTuple):
    num: int
    positions: int
    start: int

    @classmethod
    def from_str(cls, disc_str: str) -> "Disc":
        match = RE_DISC.match(disc_str)
        return cls(*map(int, match.groups()))

    @property
    def first_align(self) -> int:
        return self.positions - self.start if self.start else 0

    def aligned_at(self, time: int) -> bool:
        time += self.start
        return time % self.positions == 0

    def aligned_with_fall(self, fall_start: int) -> bool:
        return self.aligned_at(fall_start + self.num)


def find_first_align(discs: List[str]):
    discs = [Disc.from_str(string) for string in discs]
    biggest = max(discs, key=attrgetter("positions"))
    t_0 = -(biggest.start + biggest.num) % biggest.positions
    return next(
        t
        for t in count(t_0, biggest.positions)
        if all(d.aligned_with_fall(t) for d in discs)
    )


def find_second_align(discs: List[str]):
    discs = [Disc.from_str(string) for string in discs]
    discs.append(Disc(len(discs) + 1, 11, 0))
    biggest = max(discs, key=attrgetter("positions"))
    t_0 = -(biggest.start + biggest.num) % biggest.positions
    return next(
        t
        for t in count(t_0, biggest.positions)
        if all(d.aligned_with_fall(t) for d in discs)
    )


def main(data: str):
    # TODO: Use Extended Euclidean Algorithm?
    lines = data.splitlines()
    yield find_first_align(lines)
    yield find_second_align(lines)
