
from aoc_2024 import day_05

EXAMPLE = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
SORTED = [True, True, True, False, False, False]


def test_parse_input():
    rules, updates = day_05.parse_input(EXAMPLE)

    assert rules.cmp(47, 47) == 0
    assert rules.cmp(47, 53) == -1
    assert rules.cmp(53, 47) == 1

    assert len(updates) == 6
    assert updates[2] == [75, 29, 13]


def test_part_1():
    rules, updates = day_05.parse_input(EXAMPLE)
    assert day_05.sort_sums(rules, updates)[0] == 143


def test_part_2():
    rules, updates = day_05.parse_input(EXAMPLE)
    assert day_05.sort_sums(rules, updates)[1] == 123
