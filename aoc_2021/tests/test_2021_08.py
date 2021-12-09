from aoc_2021.day_08 import *

EXAMPLE_1 = """
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
"""
EXAMPLE_2 = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""


def test_solve_segment_display():
    (obs, _), = parse_data(EXAMPLE_1)
    assert solve_segment_display(obs) == {
        'a': 'C', 'b': 'F', 'c': 'G', 'd': 'A', 'e': 'B', 'f': 'D', 'g': 'E'
    }


def test_decode_number():
    (obs, digits), = parse_data(EXAMPLE_1)
    assert decode_number(obs, digits) == 5353


def test_parse_data():
    data = parse_data(EXAMPLE_1)
    assert len(data) == 1
    obs, digits = data[0]
    assert obs == ["acedgfb", "cdfbe", "gcdfa", "fbcad", "dab", "cefabd", "cdfgeb", "eafb", "cagedb", "ab"]
    assert digits == ["cdfeb", "fcadb", "cdfeb", "cdbaf"]


def test_count_1478_digits():
    data = parse_data(EXAMPLE_2)
    assert count_1478_digits(data) == 26


def test_decode_data():
    data = parse_data(EXAMPLE_2)
    assert decode_data(data) == 61229
