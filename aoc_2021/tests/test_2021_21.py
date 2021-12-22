from aoc_2021.day_21 import parse_start_pos, practice_game, dirac_game

EXAMPLE = """
Player 1 starting position: 4
Player 2 starting position: 8
"""


def test_parse_start_pos():
    assert parse_start_pos(EXAMPLE) == (4, 8)


def test_practice_game():
    assert practice_game(4, 8) == 739785


def test_dirac_game():
    assert dirac_game(4, 8) == (444356092776315, 341960390180808)


def test_small_dirac_game():
    # P1 always wins after first roll
    assert dirac_game(1, 1, 4) == (27, 0)
    # On 26/27 rolls, P1 wins on round 1.
    # If P1 rolls 3 (1/26) they'll have only 4 points.
    # Then P2 has the same case, can win round 2 in 26/27 case.
    # And in the 1/27 chance they roll a 3, P1 always wins next round.
    assert dirac_game(1, 1, 5) == (53, 26)
    # Same as above, except P2 has a 1/27 chance of rolling 9
    # which sends them to back to square 1.
    assert dirac_game(1, 2, 5) == (53, 26)
