import pytest

from aoc_2024 import day_02

EXAMPLE = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
SAFE_1 = [True, False, False, False, False, True]
SAFE_2 = [True, False, False, True, True, True]

@pytest.mark.parametrize("report,safe", zip(day_02.parse_input(EXAMPLE), SAFE_1))
def test_report_safe(report, safe):
    assert day_02.is_safe(report) is safe

@pytest.mark.parametrize("report,safe", zip(day_02.parse_input(EXAMPLE), SAFE_2))
def test_report_safe_2(report, safe):
    assert day_02.is_safe_2(report) is safe
