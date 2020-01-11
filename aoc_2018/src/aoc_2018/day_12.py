from typing import List


def grow(filters: List[int], plants: int, generations: int):
    this_gen = plants
    offset = plants.bit_length()

    def offset_incr(num):
        return [0, 2, 1, 2][num & 3]

    for i in range(generations):
        next_gen = 0
        prev_gen = this_gen
        while this_gen & 15:
            this_gen <<= 1
        for n in range(this_gen.bit_length()):
            next_gen += filters[(this_gen >> n) & 31] << n
        if next_gen == prev_gen:
            offset += offset_incr(next_gen) * (generations - i)
            break
        offset += offset_incr(next_gen)
        this_gen = next_gen
    return this_gen, offset


def parse_input(data: str):
    _trans = str.maketrans("#.", "10")

    def parse_plants(plants: str):
        return int(plants.translate(_trans), base=2)

    lines = data.splitlines()
    ini_state = parse_plants(lines[0].rsplit(maxsplit=1)[1])

    filters = [0] * 32
    for line in lines[2:]:
        if line.endswith(" => #"):
            filters[parse_plants(line[:5])] = 1
    return filters, ini_state


def print_plants(plants: int):
    binary = bin(plants)[2:]
    return binary.replace("1", "#").replace("0", ".").rstrip(".")


def count_plants(plants: int, offset: int):
    while not plants & 1:
        plants >>= 1
    indices = range(offset - plants.bit_length(), offset)
    return sum(n for p, n in zip(bin(plants)[2:], indices) if p == "1")


def main(data: str):
    filters, plants = parse_input(data)
    yield count_plants(*grow(filters, plants, 20))
    yield count_plants(*grow(filters, plants, 50_000_000_000))
