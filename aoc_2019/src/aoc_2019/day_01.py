"""
Advent of Code 2019, day 1
https://adventofcode.com/2019/day/1

For a longer explanation of the problem and my solution, read:
https://github.com/xvillaneau/adventofcode-python/wiki/AoC-2019-Day-1
"""
from typing import List

from libaoc import BaseRunner


class AocRunner(BaseRunner):
    year = 2019
    day = 1
    parser = BaseRunner.int_list_parser()

    def run(self, data: List[int]):
        """Main solution for day 1 of AoC 2019."""
        # Part 1
        yield sum(mass // 3 - 2 for mass in data)

        # Part 2
        total_fuel = 0
        for fuel in data:
            while (fuel := fuel // 3 - 2) > 0:
                total_fuel += fuel
        yield total_fuel
