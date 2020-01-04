"""
Advent of Code 2019 day 4, simple solution
https://adventofcode.com/2019/day/4

Run it with:  python run_aoc.py 2019 4 simple
Read the docs at:  /aoc_2019/docs/day_04.md
"""


def to_digits(number):
    digits = []
    while number:
        digits.append(number % 10)
        number //= 10
    return digits[::-1]


def check_password(number):
    has_pair = False

    digits = to_digits(number)
    for left, right in zip(digits, digits[1:]):
        if left > right:
            return False
        if left == right:
            has_pair = True

    return has_pair


def check_password_2(number):
    has_strict_pair = False
    streak = 1

    digits = to_digits(number)
    for left, right in zip(digits, digits[1:]):
        if left > right:
            return False
        elif left == right:
            streak += 1
        else:  # left < right
            if streak == 2:
                has_strict_pair = True
            streak = 1

    if streak == 2:
        has_strict_pair = True

    return has_strict_pair


def parse_input_range(data: str):
    """Convert the input string into start and stop values"""
    start, _, stop = data.partition("-")
    return int(start), int(stop)


def part_1(start, stop):
    """Part 1 of AoC 2019, day 4"""
    return sum(check_password(num) for num in range(start, stop + 1))


def part_2(start, stop):
    """Part 2 of AoC 2019, day 4"""
    return sum(check_password_2(num) for num in range(start, stop + 1))


def main(data):
    """Main for use by run_aoc.py"""
    start, stop = parse_input_range(data)
    yield part_1(start, stop)
    yield part_2(start, stop)


if __name__ == "__main__":
    import sys

    with open(sys.argv[1]) as file:
        _start, _stop = parse_input_range(file.read())
    print(f"Aoc 2019, day 4, part 1:", part_1(_start, _stop))
    print(f"Aoc 2019, day 4, part 2:", part_2(_start, _stop))
