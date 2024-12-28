
import pytest

from aoc_2024 import day_07

EXAMPLE = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
INPUT = day_07.parse_input(EXAMPLE)
COUNTS_1 = [1, 1, 0, 0, 0, 0, 0, 0, 1]
COUNTS_2 = [1, 1, 0, 1, 1, 0, 1, 0, 1]


@pytest.mark.parametrize("value,nums,count", zip(*zip(*INPUT), COUNTS_1))
def test_count_valid(value: int, nums: list[int], count):
    assert day_07.is_valid(value, nums) == count


@pytest.mark.parametrize("value,nums,count", zip(*zip(*INPUT), COUNTS_2))
def test_count_valid_concat(value: int, nums: list[int], count):
    assert day_07.is_valid(value, nums, concat=True) == count
