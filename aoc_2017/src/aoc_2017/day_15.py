from typing import Tuple

GEN_DIV = 2147483647
PAIR_TRIES = 40_000_000
BITS_16 = 2 ** 16 - 1


def generator(factor, start, divider=GEN_DIV, dividable=None):
    val = start
    while True:
        val = (val * factor) % divider
        if dividable is None or val % dividable == 0:
            yield val


def count_matches(gen_a, gen_b, tries=PAIR_TRIES):
    count = 0
    for _ in range(tries):
        a, b = next(gen_a), next(gen_b)
        if a & BITS_16 == b & BITS_16:
            count += 1
    return count


def part_1(starts: Tuple[int, int]):
    generator_a = generator(16807, starts[0])
    generator_b = generator(48271, starts[1])
    return count_matches(generator_a, generator_b)


def part_2(starts: Tuple[int, int]):
    generator_a_4 = generator(16807, starts[0], dividable=4)
    generator_b_8 = generator(48271, starts[1], dividable=8)
    return count_matches(generator_a_4, generator_b_8, 5_000_000)


def main(data: str):
    a, b = (int(line.rsplit(maxsplit=1)[1]) for line in data.splitlines())
    # TODO: Optimize me!
    yield part_1((a, b))
    yield part_2((a, b))
