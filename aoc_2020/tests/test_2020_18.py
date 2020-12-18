import pytest

from aoc_2020.day_18 import compute_1, compute_2

OPERATIONS = [
    ("1 + 2 * 3 + 4 * 5 + 6", 71, 231),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51, 51),
    ("2 * 3 + (4 * 5)", 26, 46),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437, 1445),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240, 669060),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632, 23340),
]


@pytest.mark.parametrize("operation,result,_", OPERATIONS)
def test_compute_1(operation, result, _):
    assert compute_1(operation) == result


@pytest.mark.parametrize("operation,_,result", OPERATIONS)
def test_compute_2(operation, _, result):
    assert compute_2(operation) == result
