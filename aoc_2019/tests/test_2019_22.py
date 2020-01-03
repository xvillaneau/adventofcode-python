import pytest
from aoc_2019.day_22 import (
    follow_card,
    parse_techniques,
    merge_techniques,
    merge_commands_n_times,
    revert_card,
)


EXAMPLES = [
    (
        "deal with increment 7\ndeal into new stack\ndeal into new stack",
        [0, 3, 6, 9, 2, 5, 8, 1, 4, 7],
    ),
    (
        "cut 6\ndeal with increment 7\ndeal into new stack",
        [3, 0, 7, 4, 1, 8, 5, 2, 9, 6],
    ),
    (
        "deal with increment 7\ndeal with increment 9\ncut -2",
        [6, 3, 0, 7, 4, 1, 8, 5, 2, 9],
    ),
    (
        "\n".join([
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
        ]),
        [9, 2, 5, 8, 1, 4, 7, 0, 3, 6],
    ),
]


@pytest.mark.parametrize("techniques,result", EXAMPLES)
def test_follow_card(techniques, result):
    commands = parse_techniques(techniques)
    for i in range(10):
        assert follow_card(commands, 10, i) == result.index(i)


@pytest.mark.parametrize("techniques,result", EXAMPLES)
def test_revert_card(techniques, result):
    commands = parse_techniques(techniques)
    for i in range(10):
        assert revert_card(commands, 10, i) == result[i]


def test_merge_commands():
    commands = parse_techniques(EXAMPLES[-1][0])
    assert merge_techniques(commands, 10) == [(2, 7), (1, 3)]


def test_merge_commands_n_times():
    commands = parse_techniques(EXAMPLES[-1][0])
    for i in range(10):
        expected = merge_techniques(commands * i, 10)
        assert merge_commands_n_times(commands, 10, i) == expected
