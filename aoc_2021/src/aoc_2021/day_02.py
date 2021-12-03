from collections import Iterable
from functools import reduce


def parse_instr(lines: list[str]) -> Iterable[tuple[str, int]]:
    for line in lines:
        if not (line := line.strip()):
            continue
        mv, n = line.split()
        yield mv, int(n)


def track_sub(moves: Iterable[tuple[str, int]]) -> tuple[int, int, int]:
    def track(state: tuple[int, int, int], instr: tuple[str, int]):
        pos, depth, aim = state
        move, val = instr
        if move == "forward":
            return pos + val, depth + val * aim, aim
        elif move == "down":
            return pos, depth, aim + val
        elif move == "up":
            return pos, depth, aim - val
        return pos, depth, aim

    return reduce(track, moves, (0, 0, 0))


def main(data: str):
    moves = parse_instr(data.splitlines())
    pos, depth, aim = track_sub(moves)
    yield pos * aim
    yield pos * depth
