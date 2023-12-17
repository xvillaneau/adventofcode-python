from aoc_2023 import day_02

EXAMPLE = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def test_parse_games():
    lines = EXAMPLE.strip().splitlines()
    games = list(day_02.parse_games(lines))

    assert len(games) == 5
    g1 = games[0]
    assert g1.id == 1
    assert len(g1.rounds) == 3
    assert g1.rounds[0] == day_02.Cubes(4, 0, 3)
    assert g1.rounds[1] == day_02.Cubes(1, 2, 6)
    assert g1.rounds[2] == day_02.Cubes(0, 2, 0)


def test_is_valid():
    lines = EXAMPLE.strip().splitlines()
    games = day_02.parse_games(lines)
    valid = [g.is_valid() for g in games]

    assert valid == [True, True, False, False, True]


def test_power():
    lines = EXAMPLE.strip().splitlines()
    games = day_02.parse_games(lines)
    powers = [g.power() for g in games]

    assert powers == [48, 12, 1560, 630, 36]
