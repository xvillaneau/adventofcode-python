"""
Advent of Code 2019, day 1, "Conventional" solution
https://adventofcode.com/2019/day/1

For a longer explanation of the problem and my solution, read:
https://github.com/xvillaneau/adventofcode-python/wiki/AoC-2019-Day-1
"""
import sys


def fuel_required(mass):
    """Amount of fuel directly needed to fly a given mass"""
    return (mass // 3) - 2


def total_fuel_required(mass):
    """Total amount of fuel needed to fly a module"""
    total_fuel = 0
    fuel = fuel_required(mass)
    while fuel > 0:
        total_fuel += fuel
        fuel = fuel_required(fuel)
    return total_fuel


def read_input_data(filename):
    """Read the list of module masses"""
    data = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                data.append(int(line))
    return data


def main(filename):
    data = read_input_data(filename)
    part_1 = sum(fuel_required(mass) for mass in data)
    print("Day 1, part 1:", part_1)
    part_2 = sum(total_fuel_required(mass) for mass in data)
    print("Day 1, part 2:", part_2)


# Will only run if this file is executed directly
if __name__ == "__main__":
    main(sys.argv[1])
