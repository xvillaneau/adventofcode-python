from aoc_2023 import day_01

EXAMPLE = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

EXAMPLE_2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


def test_calibration_values():
    data = EXAMPLE.strip().splitlines()
    values = list(day_01.calibration_values(data))
    assert values == [12, 38, 15, 77]


def test_calibration_values_spelled():
    data = EXAMPLE_2.strip().splitlines()
    values = list(day_01.calibration_values_spelled(data))
    assert values == [29, 83, 13, 24, 42, 14, 76]
