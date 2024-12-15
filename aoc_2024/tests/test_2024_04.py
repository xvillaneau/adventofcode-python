
from aoc_2024 import day_04

EXAMPLE = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

def test_count_xmas():
    grid = day_04.parse_input(EXAMPLE)
    assert day_04.count_xmas(grid) == 18


def test_count_x_mas():
    grid = day_04.parse_input(EXAMPLE)
    assert day_04.count_x_mas(grid) == 9
