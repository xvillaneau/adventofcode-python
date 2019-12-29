"""
Advent of Code 2019, day 1
https://adventofcode.com/2019/day/1

For a longer explanation of the problem and my solution, read:
https://github.com/xvillaneau/adventofcode-python/wiki/AoC-2019-Day-1
"""
from typing import List, Iterator

from libaoc import BaseRunner


def fuel_iter(mass: int) -> Iterator[int]:
    """
    Iterator that yields the consecutive fuel quantities required to
    launch a given module. The first value will be the fuel calculated
    for the module, the second is for that first fuel, as so forth
    until the fuel calculated is null or negative.
    """
    while (mass := mass // 3 - 2) > 0:
        yield mass


class AocRunner(BaseRunner):
    year = 2019
    day = 1
    parser = BaseRunner.int_list_parser()

    def run(self, data: List[int]):
        """Main solution for day 1 of AoC 2019."""
        # Create the fuel iterators for all modules
        fuel_iterators = [fuel_iter(mass) for mass in data]

        # Sum the first value of each to get the first answer
        fuel_for_modules = sum(next(fuel) for fuel in fuel_iterators)
        yield fuel_for_modules

        # Sum the rest, which is only the indirect fuel required
        fuel_for_fuel = sum(sum(fuel) for fuel in fuel_iterators)
        yield fuel_for_modules + fuel_for_fuel
