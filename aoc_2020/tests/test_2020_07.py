from aoc_2020.day_07 import contains, contained_by, parse_rules, reverse_rules

EXAMPLE = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".strip().splitlines()


def test_parse_rules():
    assert parse_rules(EXAMPLE) == {
        "light red": {"bright white": 1, "muted yellow": 2},
        "dark orange": {"bright white": 3, "muted yellow": 4},
        "bright white": {"shiny gold": 1},
        "muted yellow": {"shiny gold": 2, "faded blue": 9},
        "shiny gold": {"dark olive": 1, "vibrant plum": 2},
        "dark olive": {"faded blue": 3, "dotted black": 4},
        "vibrant plum": {"faded blue": 5, "dotted black": 6},
        "faded blue": {},
        "dotted black": {},
    }


def test_reverse_rules():
    rules = parse_rules(EXAMPLE)
    assert reverse_rules(rules) == {
        "bright white": {"light red", "dark orange"},
        "muted yellow": {"light red", "dark orange"},
        "shiny gold": {"bright white", "muted yellow"},
        "faded blue": {"muted yellow", "dark olive", "vibrant plum"},
        "dark olive": {"shiny gold"},
        "vibrant plum": {"shiny gold"},
        "dotted black": {"dark olive", "vibrant plum"},
    }


def test_contained_by():
    rules = parse_rules(EXAMPLE)
    assert contained_by(rules, "shiny gold") == {
        "bright white", "muted yellow", "light red", "dark orange"
    }


EXAMPLE_2 = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
""".strip().splitlines()


def test_contains():
    assert contains(parse_rules(EXAMPLE), "shiny gold") == 32
    assert contains(parse_rules(EXAMPLE_2), "shiny gold") == 126
