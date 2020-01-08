from itertools import islice
from typing import Iterable


def house_visits(moves: Iterable[str]):
    visited, pos = {0}, 0
    for move in moves:
        if move == "^":
            pos += 128
        elif move == "v":
            pos -= 128
        elif move == ">":
            pos += 1
        else:  # <
            pos -= 1
        visited.add(pos)
    return visited


def main(data: str):
    moves = data.strip()
    yield len(house_visits(moves))

    santa = house_visits(islice(moves, 0, None, 2))
    robot = house_visits(islice(moves, 1, None, 2))
    yield len(santa | robot)
