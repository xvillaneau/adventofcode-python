"""Matrix-related tooling"""
import numpy as np


def load_string_matrix(string: str):
    """Load a multi-line string into an array of characters"""
    return np.array([list(line) for line in string.strip().splitlines()])


def convolve_2d_3x3(matrix, pattern):
    """
    Apply a 3x3 convolution pattern to a 2D matrix.
    There are ways to make it work for other pattern sizes but I have
    not looked into it yet.
    I know SciPy does convolution, I just want to avoid needing an
    additional dependency for a single use case.
    """
    assert pattern.shape == (3, 3), "Pattern must be 3x3"
    assert matrix.ndim == 2, "Matrix must be 2D"

    # Stack Overflow Numpy dark magic that works.
    m = np.pad(matrix, 1)
    view_shape = tuple(np.subtract(m.shape, matrix.shape) + 1) + matrix.shape
    strides = m.strides + m.strides
    sub_matrices = np.lib.stride_tricks.as_strided(m, view_shape, strides)
    return np.einsum('ij,ijkl->kl', pattern, sub_matrices)
