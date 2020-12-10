from aoc_2020.day_10 import count_arrangements, count_deltas, prepare_data

EXAMPLE_1 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
EXAMPLE_2 = [
    28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
    38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3
]
prepare_data(EXAMPLE_1)
prepare_data(EXAMPLE_2)


def test_count_deltas():
    assert count_deltas(EXAMPLE_1) == (7, 5)
    assert count_deltas(EXAMPLE_2) == (22, 10)


def test_count_arrangements():
    assert count_arrangements(EXAMPLE_1) == 8
    assert count_arrangements(EXAMPLE_2) == 19208
