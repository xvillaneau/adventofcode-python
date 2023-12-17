from aoc_2023 import day_05

EXAMPLE = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def test_parse_data():
    seeds, mappers = day_05.parse_data(EXAMPLE)
    assert seeds == [79, 14, 55, 13]
    assert len(mappers) == 7


def test_mapper():
    _, mappers = day_05.parse_data(EXAMPLE)
    mapper = mappers[0]

    test_values = [
        (0, 0), (49, 49), (50, 52), (97, 99), (98, 50), (99, 51), (100, 100),
        (79, 81), (14, 14), (55, 57), (13, 13),
    ]
    for seed, soil in test_values:
        assert mapper[seed] == soil


def test_get_location():
    _, mappers = day_05.parse_data(EXAMPLE)

    test_values = [(79, 82), (14, 43), (55, 86), (13, 35)]
    for seed, loc in test_values:
        assert day_05.get_location(seed, 1, mappers) == loc


def test_map_range():
    mapper = day_05.Mapper(["100 10 10"])

    assert mapper.map_range(0, 10) == [(0, 10)]
    assert mapper.map_range(10, 20) == [(100, 110)]
    assert mapper.map_range(20, 30) == [(20, 30)]
    assert mapper.map_range(0, 20) == [(0, 10), (100, 110)]
    assert mapper.map_range(0, 30) == [(0, 10), (100, 110), (20, 30)]
    assert mapper.map_range(10, 30) == [(100, 110), (20, 30)]


def test_main():
    res = list(day_05.main(EXAMPLE))
    assert res[0] == 35
    assert res[1] == 46
