from aoc_2023 import day_03

EXAMPLE = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip()


def test_main():
    res = list(day_03.main(EXAMPLE))
    assert res[0] == 4361
    assert res[1] == 467835
