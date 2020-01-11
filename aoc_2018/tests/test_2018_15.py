import pytest
from aoc_2018.day_15 import Game, optimize_elf_attack

TEST_1 = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
"""

TEST_2 = """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
"""

TEST_3 = """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
"""

TEST_4 = """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
"""

TEST_5 = """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
"""

TEST_6 = """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
"""

TEST_7 = """
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
"""

RESULTS = [
    (TEST_1, 47, 27730),
    (TEST_2, 37, 36334),
    (TEST_3, 46, 39514),
    (TEST_4, 35, 27755),
    (TEST_5, 54, 28944),
    (TEST_6, 20, 18740),
]


@pytest.mark.parametrize("start,rounds,outcome", RESULTS)
def test_game(start, rounds, outcome):
    game = Game(start)
    game.play()
    assert game.rounds == rounds
    assert game.score == outcome


P2_RESULTS = [
    (TEST_1, 15, 4988),
    (TEST_3, 4, 31284),
    (TEST_4, 15, 3478),
    (TEST_5, 12, 6474),
    (TEST_6, 34, 1140),
]


@pytest.mark.parametrize("start,attack,outcome", P2_RESULTS)
def test_optimize_attack(start, attack, outcome):
    assert optimize_elf_attack(start) == (attack, outcome)
