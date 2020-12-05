from aoc_2020.day_05 import seat_id


def test_seat_id():
    assert seat_id("FBFBBFFRLR") == 357
    assert seat_id("BFFFBBFRRR") == 567
    assert seat_id("FFFBBBFRRR") == 119
    assert seat_id("BBFFBBFRLL") == 820
