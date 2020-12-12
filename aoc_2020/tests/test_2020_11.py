import numpy as np

from aoc_2020.day_11 import (
    iterate, iterate_2, parse_seats, print_seats, run_til_stable
)

EXAMPLE = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""".strip()


def test_print_seats():
    seats, floor = parse_seats(EXAMPLE)
    assert print_seats(seats, floor) == EXAMPLE

    seats = iterate(seats, floor)
    seats = iterate(seats, floor)
    assert np.all(seats == parse_seats(print_seats(seats, floor))[0])
    assert np.all(floor == parse_seats(print_seats(seats, floor))[1])


def test_run_til_stable():
    seats, floor = parse_seats(EXAMPLE)
    stable = run_til_stable(seats, floor, iterate)
    assert np.sum(stable) == 37


def test_run_part_2():
    seats, floor = parse_seats(EXAMPLE)
    stable = run_til_stable(seats, floor, iterate_2)
    assert np.sum(stable) == 26
