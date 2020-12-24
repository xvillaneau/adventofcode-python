from aoc_2020.day_24 import *


EXAMPLE = """
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""".strip().splitlines()


def test_count_tiles():
    assert np.sum(map_tiles(EXAMPLE)) == 10


def test_flip_tiles():
    tiles = map_tiles(EXAMPLE)
    assert np.sum(tiles := flip_tiles(tiles)) == 15
    assert np.sum(tiles := flip_tiles(tiles)) == 12
    assert np.sum(flip_tiles(tiles)) == 25


def test_day_100():
    tiles = map_tiles(EXAMPLE)
    assert np.sum(day_100(tiles)) == 2208
