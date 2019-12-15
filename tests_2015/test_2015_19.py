from aoc_2015.day_19 import part_2, parse_input, fewest_transforms

example = """
e => H
e => O
H => HO
H => OH
O => HH

HOH
"""

def test_part_2():
    repl, mol = parse_input(example, reverse=True)
    assert len(fewest_transforms(repl, mol)) == 4
    assert len(fewest_transforms(repl, "HOHOHO")) == 7
    assert part_2(example) == 3

    fewest_transforms(repl, "HHOOHHOHOOHHOOO")
