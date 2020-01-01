"""
Advent of Code 2019, day 1, "Conventional" solution
https://adventofcode.com/2019/day/1

Run it with:  python run_aoc.py 2019 1 standalone
Read the docs at:  /aoc_2019/docs/day_01.md
"""


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


def read_input_data(data):
    """Read the list of module masses"""
    numbers = []
    for line in data.splitlines():
        numbers.append(int(line))
    return numbers


def main(data):
    data = read_input_data(data)
    yield sum(fuel_required(mass) for mass in data)
    yield sum(total_fuel_required(mass) for mass in data)


# Will only run if this file is executed directly
if __name__ == "__main__":
    import sys

    with open(sys.argv[1]) as file:
        _main = main(file.read())
    print(f"Aoc 2019, day 2, part 1:", next(_main))
    print(f"Aoc 2019, day 2, part 2:", next(_main))
