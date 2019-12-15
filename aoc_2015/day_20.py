from collections import defaultdict
from itertools import count
from libaoc.primes import all_factors

def n_presents_1(house: int):
    return sum(all_factors(house)) * 10

def presents_by_house(start=1, incr=1):
    for house in count(start, incr):
        yield n_presents_1(house)

def part_1(n_presents, step=1):
    return next(
        n * step for n, presents in enumerate(presents_by_house(step, step))
        if presents >= n_presents
    )

def n_presents_2(house: int):
    return sum(
        n for n in all_factors(house)
        if house // n <= 50
    ) * 11

def part_2(n_presents: int):
    return next(
        house for house in count(1)
        if n_presents_2(house) >= n_presents
    )

if __name__ == '__main__':
    from libaoc import simple_main, static_input
    simple_main(2015, 20, static_input(33100000), part_1, part_2)
