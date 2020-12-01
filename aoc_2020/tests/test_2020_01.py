from aoc_2020.day_01 import find_2020_sums

def test_202_day_01():
    example = [1721, 979, 366, 299, 675, 1456]

    assert find_2020_sums(example) == (514579, 241861950)
