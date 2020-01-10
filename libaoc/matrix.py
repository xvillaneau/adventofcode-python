"""Matrix-related tooling"""
import numpy as np


def load_string_matrix(string: str):
    """Load a multi-line string into an array of characters"""
    return np.array([list(line) for line in string.strip().splitlines()])


def convolve_2d(matrix, pattern, pad=1):
    """
    Apply a 3x3 convolution pattern to a 2D matrix.
    There are ways to make it work for other pattern sizes but I have
    not looked into it yet.
    I know SciPy does convolution, I just want to avoid needing an
    additional dependency for a single use case.
    """
    assert matrix.ndim == pattern.ndim == 2, "Matrix must be 2D"

    # Stack Overflow Numpy dark magic that works.
    if pad:
        matrix = np.pad(matrix, pad)

    dx, dy = matrix.shape
    px, py = pattern.shape

    view_shape = (px, py, dx - px + 1, dy - py + 1)
    strides = matrix.strides + matrix.strides
    sub_matrices = np.lib.stride_tricks.as_strided(matrix, view_shape, strides)
    return np.einsum('ij,ijkl->kl', pattern, sub_matrices)
