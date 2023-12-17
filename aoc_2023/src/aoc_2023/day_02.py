import re
from collections.abc import Iterator
import dataclasses


RE_LINE = re.compile(r"^Game (\d+): (.*)")


@dataclasses.dataclass
class Cubes:
    red: int
    green: int
    blue: int

    @classmethod
    def parse(cls, text: str) -> "Cubes":
        c = {"red": 0, "green": 0, "blue": 0}
        for cnt in text.split(","):
            n, color = cnt.split()
            c[color] += int(n)
        return Cubes(c["red"], c["green"], c["blue"])

    def includes(self, other: "Cubes") -> bool:
        return (
            self.red >= other.red and
            self.green >= other.green and
            self.blue >= other.blue)


@dataclasses.dataclass
class Game:
    id: int
    rounds: list[Cubes]

    @classmethod
    def parse(cls, line: str) -> "Game":
        match = RE_LINE.fullmatch(line)
        num, games_str = match.groups()
        games = [Cubes.parse(t) for t in games_str.split(";")]
        return Game(int(num), games)

    def is_valid(self) -> bool:
        return all(LIMIT.includes(rd) for rd in self.rounds)

    def power(self) -> int:
        mr, mg, mb = 0, 0, 0
        for r in self.rounds:
            mr = max(mr, r.red)
            mg = max(mg, r.green)
            mb = max(mb, r.blue)
        return mr * mg * mb


LIMIT = Cubes(12, 13, 14)


def parse_games(data: list[str]) -> Iterator[Game]:
    for line in data:
        yield Game.parse(line)


def main(data: str):
    lines = data.strip().splitlines()
    games = list(parse_games(lines))
    yield sum(g.id for g in games if g.is_valid())
    yield sum(g.power() for g in games)
