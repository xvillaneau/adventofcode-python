from aoc_2018.day_12 import parse_input, count_plants, grow

EXAMPLE = """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
""".lstrip()


def test_grow():
    filters, plants = parse_input(EXAMPLE)
    assert count_plants(*grow(filters, plants, 20)) == 325
