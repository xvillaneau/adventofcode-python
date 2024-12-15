import numpy as np

from libaoc.matrix import convolve_2d, load_string_matrix


def parse_input(data: str):
    data = data.translate(str.maketrans('XMAS', '0123'))
    letters = load_string_matrix(data)
    powers = letters.astype("int16")
    return np.power(5, powers)


def count_xmas(grid) -> int:
    pat_l = np.array([[1, 5, 25, 125]])
    pat_d = np.diag(pat_l[0])
    dirs = (
        pat_l, pat_l[:,::-1], pat_l.transpose(), pat_l[:,::-1].transpose(),
        pat_d, pat_d[:,::-1], pat_d[::-1,:], pat_d[::-1,::-1],
    )
    return sum(
        np.sum(np.logical_and(convolve_2d(grid, p) == 16276, convolve_2d(grid, p > 0) == 156))
        for p in dirs
    )


def count_x_mas(grid) -> int:
    m0 = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    m1 = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 1]])
    m2 = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]])

    return np.sum(
        np.sum(np.array([
            convolve_2d(grid, m0) == 25,
            convolve_2d(grid, m1) == 130,
            convolve_2d(grid, m2) == 130,
        ]), axis=0) == 3
    )


def main(data: str):
    grid = parse_input(data)
    yield count_xmas(grid)
    yield count_x_mas(grid)
