from aoc_2021.day_14 import parse_data, polymer_delta

EXAMPLE = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

def test_parse_data():
    template, pairs = parse_data(EXAMPLE)
    assert template == "NNCB"
    assert len(pairs) == 16


def test_polymer_delta_10():
    polymer, pairs = parse_data(EXAMPLE)
    assert polymer_delta(polymer, pairs, 10) == 1588


def test_polymer_delta_40():
    polymer, pairs = parse_data(EXAMPLE)
    assert polymer_delta(polymer, pairs, 40) == 2188189693529
