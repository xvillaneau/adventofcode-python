from aoc_2021.day_06 import count_all_fish


def test_count_all_fish():
    assert count_all_fish([3, 4, 3, 1, 2], 80) == 5934
    assert count_all_fish([3, 4, 3, 1, 2], 256) == 26984457539
