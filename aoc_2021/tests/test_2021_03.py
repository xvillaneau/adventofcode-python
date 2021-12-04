from aoc_2021.day_03 import gamma_epsilon_rates, get_ratings, parse_bits

EXAMPLE = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""


def test_parse_bits():
    codes = parse_bits(EXAMPLE)
    assert len(codes) == 12
    assert codes[0] == [0, 0, 1, 0, 0]


def test_gamma_epsilon_rates():
    codes = parse_bits(EXAMPLE)
    assert gamma_epsilon_rates(codes) == (22, 9)


def test_get_ratings():
    codes = parse_bits(EXAMPLE)
    assert get_ratings(codes) == (23, 10)
