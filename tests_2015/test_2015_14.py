from aoc_2015.day_14 import calc_distance, max_distance, max_points

example = [
    "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
    "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.",
]

def test_distance():
    assert calc_distance(1000, 14, 10, 127) == 1120
    assert calc_distance(1000, 16, 11, 162) == 1056

def test_max_distance():
    assert max_distance(example, 1000) == 1120

def test_max_points():
    assert max_points(example, 1000) == 689
