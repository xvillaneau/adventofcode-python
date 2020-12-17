from aoc_2020.day_17 import boot_sequence, parse_start

EXAMPLE = """
.#.
..#
###
""".strip()


def test_boot_sequence():
    assert boot_sequence(parse_start(EXAMPLE, dims=3)) == 112
    assert boot_sequence(parse_start(EXAMPLE, dims=4)) == 848
