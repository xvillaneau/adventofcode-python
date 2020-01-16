import pytest
from aoc_2016.day_18 import next_row, count_safe_tiles

example_1 = """
..^^.
.^^^^
^^..^
""".strip().splitlines()

example_2 = """
.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^
""".strip().splitlines()


@pytest.mark.parametrize("pattern", [example_1, example_2])
def test_next_row(pattern):
    row = pattern[0]
    for line in pattern[1:]:
        row = next_row(row)
        assert row == line


def test_count_safe_tiles():
    assert count_safe_tiles(example_1[0], 3) == 6
    assert count_safe_tiles(example_2[0], 10) == 38
