import numpy as np

from libaoc.matrix import convolve_2d


def make_power_levels(serial_number: int):
    coords = np.mgrid[1:301][:, np.newaxis]
    power_levels = (coords + 10) @ coords.transpose()
    power_levels += serial_number
    power_levels *= coords + 10
    power_levels //= 100
    power_levels %= 10
    power_levels -= 5
    return power_levels


def total_power(power_levels, square=3):
    power_sums = convolve_2d(power_levels, np.ones((square, square), dtype=int), 0)
    x, y = np.unravel_index(power_sums.argmax(), power_sums.shape)
    return x + 1, y + 1, power_sums[x, y]


def best_square(power_levels):
    # TODO: Very slow, find ways to optimize
    best_score, best_result = 0, (0, 0, 0)
    for square in range(1, 301):
        x, y, score = total_power(power_levels, square)
        if score > best_score:
            best_result = x, y, square
            best_score = score
    return best_result


def main(data: int):
    powers = make_power_levels(int(data))
    x1, y1, _ = total_power(powers)
    yield f"{x1},{y1}"

    yield "Part 2 is too slow, fix it!"
    # x2, y2, s2 = best_square(powers)
    # yield f"{x2},{y2},{s2}"
