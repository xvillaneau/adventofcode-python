import numpy as np
from scipy.signal import convolve2d

from libaoc.matrix import load_string_matrix

FILTER = np.array([[1, 2, 4], [8, 16, 32], [64, 128, 256]])


def parse_data(data: str) -> tuple[np.ndarray, np.ndarray]:
    alg, _, mat = data.strip().partition("\n\n")
    alg = alg.strip().replace("\n", "")
    mat = load_string_matrix(mat)
    return np.array(list(alg)) == "#", mat == "#"


def enhance(algorithm: np.ndarray, image: np.ndarray, fill: bool):
    indices = convolve2d(image, FILTER, fillvalue=fill)
    new_fill = algorithm[511 * fill]
    return algorithm[indices], new_fill


def main(data: str):
    alg, mat = parse_data(data)
    mat, fill = enhance(alg, mat, False)
    mat, fill = enhance(alg, mat, fill)
    yield np.sum(mat)

    for _ in range(48):
        mat, fill = enhance(alg, mat, fill)
    yield np.sum(mat)
