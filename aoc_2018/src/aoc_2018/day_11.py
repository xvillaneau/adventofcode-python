
import numpy as np


def gen_powers(sn: int):
    y_coords = np.repeat(np.arange(300)[np.newaxis], 300, 0) + 1
    x_coords = y_coords.transpose()
    rack_ids = x_coords + 10
    return ((((rack_ids * y_coords + sn) * rack_ids) // 100) % 10) - 5


def total_power(powers, square=3, print_size=False):
    # TODO: Fix me
    pow_sums = convolve(powers, np.ones((square, square), dtype=int), mode='valid')
    x, y = divmod(pow_sums.argmax(), (300 - square + 1))
    out_str = f'{x+1},{y+1},{square}' if print_size else f'{x+1},{y+1}'
    return out_str, pow_sums.max()


def best_square(sn: int):
    powers = gen_powers(sn)
    res_1 = total_power(powers)[0]

    best_score, res_2 = 0, ""
    for square in range(1, 301):
        res, score = total_power(powers, square, print_size=True)
        if score > best_score:
            best_score, res_2 = score, res
    return res_1, res_2


if __name__ == '__main__':
    from libaoc import tuple_main
    tuple_main(2018, 11, lambda x, y: 6878, best_square)
