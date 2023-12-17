import numpy as np
import scipy as sp

from libaoc.matrix import load_string_matrix


def compute_values(mat):
    # Mask of where we have digits in the schematic
    digits_mask = (mat >= '0') & (mat <= '9')
    # Convert the Unicode digits to integers
    digits = np.where(digits_mask, mat.view("uint32") - ord('0'), 0)
    # Shift the digits to the right to have the tens and hundreds.
    # We do this in steps with masks to avoid numbers overlapping
    tens = np.roll(digits, 1, 1) * digits_mask
    hundreds = np.roll(tens, 1, 1) * digits_mask
    # Mask of where each number has its least-significant digit
    lsd_mask = digits_mask ^ sp.ndimage.binary_erosion(digits_mask, [[0, 1, 1]])
    # Sum all the values, and place them where the least-significant digits were
    return (digits + 10 * tens + 100 * hundreds) * lsd_mask


def main(data: str):
    mat = load_string_matrix(data)
    values = compute_values(mat)

    # Observation: numbers in the schematic are:
    #  1. NEVER adjacent to each other
    #  2. have always ZERO or ONE adjacent symbols
    # So by labeling continuous regions (including diagonals) we put a label (number)
    # on each group of numbers/symbols, and each group should have zero or one symbol.
    labels, _ = sp.ndimage.label(mat != '.', np.ones((3, 3)))

    regions: dict[int, tuple[str, list[int]]] = {}

    # Iterate over the symbols and keep track of each symbol's label
    symbols_mask = (mat != '.') & (mat < '0')
    sym_labels = np.extract(symbols_mask, labels)
    sym_ordered = np.extract(symbols_mask, mat)
    for label, sym in zip(sym_labels, sym_ordered):
        if label in regions:
            raise ValueError("duplicate label!!")
        regions[label] = (sym, [])

    parts = 0
    # Iterate over the numbers, assign them to each recorded symbol
    val_labels = np.extract(values > 0, labels)
    val_ordered = np.extract(values > 0, values)
    for label, val in zip(val_labels, val_ordered):
        if label not in regions:
            continue
        parts += val
        regions[label][1].append(val)

    # Sum of all numbers adjacent to a symbol
    yield parts

    # Sum all the pairs of gears
    gears = 0
    for sym, values in regions.values():
        if sym != "*" or len(values) != 2:
            continue
        gears += values[0] * values[1]
    yield gears
