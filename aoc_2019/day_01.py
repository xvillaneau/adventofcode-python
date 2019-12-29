"""
Advent of Code 2019, day 1
https://adventofcode.com/2019/day/1

For a longer explanation of the problem and my solution, read:
https://github.com/xvillaneau/adventofcode-python/wiki/AoC-2019-Day-1
"""
from typing import List, Iterator


def fuel_iter(mass: int) -> Iterator[int]:
    """
    Iterator that yields the consecutive fuel quantities required to
    launch a given module. The first value will be the fuel calculated
    for the module, the second is for that first fuel, as so forth
    until the fuel calculated is null or negative.
    """
    while (mass := mass // 3 - 2) > 0:
        yield mass


def sum_fuel(modules: List[int]) -> int:
    """
    Fuel required for the modules alone. This is done by only taking
    the first value returned by the iterator.
    """
    return sum(next(fuel_iter(mod)) for mod in modules)


def sum_adjusted(modules: List[int]) -> int:
    """
    Total fuel required, including the fuel mass. This is done by
    summing all the values from each iterator together.
    """
    return sum(sum(fuel_iter(mod)) for mod in modules)


if __name__ == '__main__':
    from libaoc import files, simple_main
    simple_main(2019, 1, files.read_int_list, sum_fuel, sum_adjusted)
