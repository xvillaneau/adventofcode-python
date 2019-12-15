from itertools import islice
from aoc_2019.day_10 import Field, Pt, analyze_asteroids, day_10, find_station, exterminate

example_1 = """
.#..#
.....
#####
....#
...##
"""

example_2 = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""

example_3 = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""

example_4 = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""

example_5 = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

def test_load_asteroids():
    coords = {
        (1, 0), (4, 0), (0, 2), (1, 2), (2, 2),
        (3, 2), (4, 2), (4, 3), (3, 4), (4, 4),
    }
    assert Field.from_map(example_1) == (coords, 5, 5)

def test_analyze():
    field = Field.from_map(example_1)
    res = analyze_asteroids(field)
    sight_counts = {
        Pt(1, 0): 7,
        Pt(4, 0): 7,
        Pt(0, 2): 6,
        Pt(1, 2): 7,
        Pt(2, 2): 7,
        Pt(3, 2): 7,
        Pt(4, 2): 5,
        Pt(4, 3): 7,
        Pt(3, 4): 8,
        Pt(4, 4): 7,
    }
    for pt, sight in res.items():
        assert len(sight) == sight_counts[pt]

def test_part_1():
    assert next(day_10(example_1)) == 8
    assert next(day_10(example_2)) == 33
    assert next(day_10(example_3)) == 35
    assert next(day_10(example_4)) == 41
    assert next(day_10(example_5)) == 210

def test_points_sort():
    station = Pt(8, 3)
    destroyed = {
        Pt(9, 0), Pt(10, 0), Pt(8, 1), Pt(9, 1), Pt(11, 1),
        Pt(12, 1), Pt(15, 1), Pt(9, 2), Pt(11, 2),
    }
    assert sorted(destroyed, key=lambda p: p - station) == [
        (8, 1), (9, 0), (9, 1), (10, 0), (9, 2),
        (11, 1), (12, 1), (11, 2), (15, 1),
    ]

def test_vaporize():
    field = Field.from_map(example_5)
    sight_scores = analyze_asteroids(field)
    station = find_station(sight_scores)

    vaporize_iter = exterminate(field, sight_scores[station], station)
    assert next(vaporize_iter) == (11, 12)
    assert next(vaporize_iter) == (12, 1)
    assert next(vaporize_iter) == (12, 2)
    assert next(islice(vaporize_iter, 6, None)) == (12, 8)  # 10th
    assert next(islice(vaporize_iter, 9, None)) == (16, 0)  # 20th
    assert next(islice(vaporize_iter, 29, None)) == (16, 9)  # 50th
    assert next(islice(vaporize_iter, 49, None)) == (10, 16)  # 100th
    assert next(islice(vaporize_iter, 98, None)) == (9, 6)  # 199th
    assert next(vaporize_iter) == (8, 2)  # 200th
    assert next(vaporize_iter) == (10, 9)  # 201th

def test_day_10():
    assert tuple(day_10(example_5)) == (210, 802)
