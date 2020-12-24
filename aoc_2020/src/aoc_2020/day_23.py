from collections import deque
from typing import Optional


def play(cups: list[int], rounds=100):
    cups = deque(cups)
    size = len(cups)
    picks: list[Optional[tuple[int, int, int]]] = [None] * (size + 1)

    # These methods are called so many times that declaring them locally
    # (which allows load_fast in the bytecode) feels faster.
    rot, ext, pop = cups.rotate, cups.extendleft, cups.pop

    for _ in range(rounds):
        for _ in range(4):
            rot(-1)
            head = cups[-1]
            if (pick := picks[head]) is not None:
                ext(pick)
                picks[head] = None

        picked = (pop(), pop(), pop())

        destination = current = cups[-1]
        while destination in {current, *picked}:
            destination = 1 + (destination - 2) % size

        picks[destination] = picked

    last_picks = {i: p for i, p in enumerate(picks) if p is not None}
    while last_picks:
        rot(-1)
        ext(last_picks.pop(cups[-1], ()))

    return list(cups)


def labels(cups: list[int]) -> str:
    pos_1 = cups.index(1)
    return ''.join(str(n) for n in cups[pos_1 + 1:] + cups[:pos_1])


def cups_at_1(cups: list[int]) -> int:
    pos_1 = cups.index(1)
    size = len(cups)
    return cups[(pos_1 + 1) % size] * cups[(pos_1 + 2) % size]


def main(data: str):
    cups = [int(n) for n in data.strip()]
    yield labels(play(cups))

    many_cups = cups + list(range(10, 1_000_001))
    yield cups_at_1(play(many_cups, 10_000_000))
