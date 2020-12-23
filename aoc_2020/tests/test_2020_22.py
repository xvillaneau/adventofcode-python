from aoc_2020.day_22 import *

EXAMPLE = """
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""".strip()


def test_parse_deck():
    d1, d2 = parse_deck(EXAMPLE)
    assert d1 == deque([9, 2, 6, 3, 1])
    assert d2 == deque([5, 8, 4, 7, 10])


def test_play_round():
    d1, d2 = parse_deck(EXAMPLE)

    play_round(d1, d2)
    assert d1 == deque([2, 6, 3, 1, 9, 5])
    assert d2 == deque([8, 4, 7, 10])

    play_round(d1, d2)
    assert d1 == deque([6, 3, 1, 9, 5])
    assert d2 == deque([4, 7, 10, 8, 2])


def test_play_game():
    d1, d2 = parse_deck(EXAMPLE)
    winner = play_game(d1, d2)
    assert winner == deque([3, 2, 10, 6, 8, 5, 9, 4, 7, 1])


def test_score():
    deck = deque([3, 2, 10, 6, 8, 5, 9, 4, 7, 1])
    assert score(deck) == 306


def test_infinite_game():
    d1, d2 = (43, 19), (2, 29, 14)
    assert play_recursive_game(d1, d2)[0]  # P1 wins


def test_recursive_game():
    d1, d2 = parse_deck(EXAMPLE)
    p1_wins, winner = play_recursive_game(tuple(d1), tuple(d2))
    assert not p1_wins
    assert winner == (7, 5, 6, 2, 4, 1, 10, 8, 9, 3)
