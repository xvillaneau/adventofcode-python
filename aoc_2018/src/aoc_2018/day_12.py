
import numpy as np

TEST = """
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
""".strip().splitlines()


def parse_input_vest(vect_str):
    return np.array([1 if c == '#' else -1 for c in vect_str], dtype=int)


def generation(filters, plants):
    return np.array([
        np.convolve(np.pad(plants, (4, 4), mode='constant', constant_values=-1),
                    p_filter[::-1], mode='valid') == 5 for p_filter in filters
    ]).sum(axis=0) * 2 - 1


def many_gens(filters, plants_ini, generations=20):
    plants = plants_ini
    for _ in range(generations):
        plants = generation(filters, plants)
    return plants


def parse_input(lines):
    i_lines = iter(lines)
    ini_state = parse_input_vest(next(i_lines)[15:])
    next(i_lines)
    filters = np.array([parse_input_vest(l[:5]) for l in i_lines if l.endswith(' => #')])
    return filters, ini_state


def as_str(plants):
    has_plants = np.trim_zeros(plants == 1)
    return ''.join(map(['.', '#'].__getitem__, has_plants))


def main(data: str, generations=20):
    filters, plants = parse_input(data.splitlines())
    res = (many_gens(filters, plants, generations) + 1) // 2
    yield (res * (np.arange(len(res)) - 2 * generations)).sum()
