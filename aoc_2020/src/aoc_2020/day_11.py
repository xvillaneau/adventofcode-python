import numpy as np

from libaoc.matrix import convolve_2d, load_string_matrix

FILTER = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def parse_seats(seats: str):
    raw_seats = load_string_matrix(seats)
    return (raw_seats == '#'), (raw_seats == '.')


def iterate(seats, floor):
    counts = convolve_2d(seats, FILTER)
    new_seats, empty_seats = (counts == 0), (counts >= 4)
    return (seats | new_seats) & (~empty_seats) & (~floor)


def iterate_2(seats, floor):
    counts = np.zeros(seats.shape)

    for _ in range(4):
        floor = np.rot90(floor)
        seats = np.rot90(seats)
        counts = np.rot90(counts)

        diag = np.zeros(counts.shape, dtype=bool)
        vert = np.zeros(counts.shape, dtype=bool)
        for (x, y), f in np.ndenumerate(floor):
            if x and y:
                diag[x, y] = diag[x-1, y-1] if floor[x-1, y-1] else seats[x-1, y-1]
            if x:
                vert[x, y] = vert[x-1, y] if floor[x-1, y] else seats[x-1, y]
        counts += diag
        counts += vert

    new_seats, empty_seats = (counts == 0), (counts >= 5)
    return (seats | new_seats) & (~empty_seats) & (~floor)


def print_seats(seats, floor):
    img = np.where(seats, '#', 'L')
    img = np.where(floor, '.', img)
    return '\n'.join(''.join(ln) for ln in img)


def run_til_stable(seats, floor, iter_func):
    this_state = print_seats(seats, floor)
    prev_state = ''
    while this_state != prev_state:
        prev_state = this_state
        seats = iter_func(seats, floor)
        this_state = print_seats(seats, floor)

    return seats


def main(data: str):
    seats, floor = parse_seats(data)
    yield np.sum(run_til_stable(seats, floor, iterate))
    yield np.sum(run_til_stable(seats, floor, iterate_2))
