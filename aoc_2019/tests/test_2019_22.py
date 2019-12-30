import numpy as np
import pytest
from aoc_2019.day_22 import (
    deal_with_increment,
    deal_new_stack,
    cut_stack,
    follow_card,
    parse_techniques,
    merge_commands,
    merge_commands_n_times,
    revert_card,
)


def test_deal_new_stack():
    deck = np.arange(10)
    assert list(deal_new_stack(deck)) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


def test_cut():
    deck = np.arange(10)
    assert list(cut_stack(deck, 3)) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert list(cut_stack(deck, -4)) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]


def test_deal_with_increment():
    deck = np.arange(10)
    assert list(deal_with_increment(deck, 3)) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]


EXAMPLES = [
    (
        ["deal with increment 7", "deal into new stack", "deal into new stack"],
        [0, 3, 6, 9, 2, 5, 8, 1, 4, 7],
    ),
    (
        ["cut 6", "deal with increment 7", "deal into new stack"],
        [3, 0, 7, 4, 1, 8, 5, 2, 9, 6],
    ),
    (
        ["deal with increment 7", "deal with increment 9", "cut -2"],
        [6, 3, 0, 7, 4, 1, 8, 5, 2, 9],
    ),
    (
        [
            "deal into new stack",
            "cut -2",
            "deal with increment 7",
            "cut 8",
            "cut -4",
            "deal with increment 7",
            "cut 3",
            "deal with increment 9",
            "deal with increment 3",
            "cut -1",
        ],
        [9, 2, 5, 8, 1, 4, 7, 0, 3, 6],
    ),
]


@pytest.mark.parametrize("techniques,result", EXAMPLES)
def test_follow_card(techniques, result):
    commands = parse_techniques(techniques)
    for i in range(10):
        assert follow_card(commands, i, 10) == result.index(i)


@pytest.mark.parametrize("techniques,result", EXAMPLES)
def test_revert_card(techniques, result):
    commands = parse_techniques(techniques)
    for i in range(10):
        assert revert_card(commands, i, 10) == result[i]


def test_merge_commands():
    commands = parse_techniques(EXAMPLES[-1][0])
    assert merge_commands(commands, 10) == [(2, 7), (1, 3)]


def test_merge_commands_n_times():
    commands = parse_techniques(EXAMPLES[-1][0])
    for i in range(10):
        expected = merge_commands(commands * i, 10)
        assert merge_commands_n_times(commands, 10, i) == expected
