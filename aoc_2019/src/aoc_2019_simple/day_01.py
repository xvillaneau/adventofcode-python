"""
Advent of Code 2019 day 1, simple solution
https://adventofcode.com/2019/day/1

Run it with:  python run_aoc.py 2019 1 simple
Read the docs at:  /aoc_2019/docs/day_01.md
"""


def read_input_data(filename):
    """Get the contents of a file"""
    with open(filename, "r") as file:
        return file.read()


def process_data(data):
    """Parse the input text into a list of numbers"""
    lines = data.splitlines()
    numbers = []
    for line in lines:
        number = int(line)
        numbers.append(number)
    return numbers


def fuel_required(mass):
    """Amount of fuel directly needed to fly a given mass"""
    return (mass // 3) - 2


def part_1(data):
    """Solve part 1 of the problem"""
    modules = process_data(data)
    return sum(fuel_required(mass) for mass in modules)


def total_fuel_required(mass):
    """Total amount of fuel needed to fly a module"""
    fuel = fuel_required(mass)
    total_fuel = 0
    while fuel > 0:
        total_fuel += fuel
        fuel = fuel_required(fuel)
    return total_fuel


def part_2(data):
    """Solve part 2 of the problem"""
    modules = process_data(data)
    return sum(total_fuel_required(mass) for mass in modules)


def main(data):
    """Run the full puzzle; this"""
    yield part_1(data)
    yield part_2(data)


# Will only run if this file is executed directly
if __name__ == "__main__":
    import sys

    _data = read_input_data(sys.argv[1])
    print(f"Aoc 2019, day 1, part 1:", part_1(_data))
    print(f"Aoc 2019, day 1, part 2:", part_2(_data))
