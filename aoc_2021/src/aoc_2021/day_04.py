from operator import itemgetter

import numpy as np

from libaoc.parsers import parse_integer_list, parse_integer_table

Board = np.ndarray


def parse_input(data: str) -> tuple[list[int], list[Board]]:
    draw, *boards = data.split("\n\n")
    draw = parse_integer_list(draw, delimiter=",")
    boards = [parse_integer_table(b) for b in boards]
    return draw, boards


def get_rows_cols(board: Board) -> list[set[int]]:
    rows = [set(r) for r in board]
    cols = [set(c) for c in board.transpose()]
    return rows + cols


def run_board(draw: list[int], board: Board) -> tuple[int, int]:
    rows_cols = get_rows_cols(board)
    assert all(len(rc) == 5 for rc in rows_cols)

    for rounds, num in enumerate(draw, start=1):
        for rc in rows_cols:
            rc.discard(num)
        if any(len(rc) == 0 for rc in rows_cols):
            score = sum(sum(rc) for rc in rows_cols[:5])
            return rounds, num * score

    return 0, 0


def run_game(draw: list[int], boards: list[Board]) -> list[int]:
    results = (run_board(draw, b) for b in boards)
    results = ((r, s) for r, s in results if r > 0)
    return [s for _, s in sorted(results, key=itemgetter(0))]


def main(data: str):
    draw, boards = parse_input(data)
    scores = run_game(draw, boards)
    yield scores[0]
    yield scores[-1]
