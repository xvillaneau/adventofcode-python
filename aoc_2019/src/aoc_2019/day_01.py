"""
Advent of Code 2019, day 1
https://adventofcode.com/2019/day/1

Run it with:  python run_aoc.py 2019 1
Read the docs at:  /aoc_2019/docs/day_01.md
"""
from libaoc.parsers import parse_integer_list


def main(data: str):
    numbers = parse_integer_list(data)

    # Part 1
    yield sum(mass // 3 - 2 for mass in numbers)

    # Part 2
    total_fuel = 0
    for fuel in numbers:
        while (fuel := fuel // 3 - 2) > 0:
            total_fuel += fuel
    yield total_fuel
