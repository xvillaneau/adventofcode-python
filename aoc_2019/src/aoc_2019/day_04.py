"""
Advent of Code 2019 day 4
https://adventofcode.com/2019/day/4

Run it with:  python run_aoc.py 2019 4
Read the docs at:  /aoc_2019/docs/day_04.md
"""


def part_1(start: int, stop: int):
    # Most significant digits of the range. Knowing this allows us
    # to narrow the explored digits even further.
    start_top, stop_top = start // 100_000, stop // 100_000

    def inner(number: int, magnitude: int, has_pair: bool):
        """Recursive generator that returns valid codes"""
        next_magnitude = magnitude * 10
        last_digit = number // magnitude

        if next_magnitude == 100_000:
            # We've reached the sixth digit: run the final step
            for digit in range(start_top, min(stop_top, last_digit) + 1):
                num = number + digit * next_magnitude
                if not start <= num <= stop:
                    continue
                if has_pair or digit == last_digit:
                    yield num

        else:
            # Still building up the number: do next layer of calls
            for digit in range(start_top, last_digit + 1):
                num = number + digit * next_magnitude
                yield from inner(num, next_magnitude, has_pair or digit == last_digit)

    # Count how many codes were yielded
    return sum(True for i in range(10) for _ in inner(i, 1, False))


def part_2(start: int, stop: int):
    start_top, stop_top = start // 100_000, stop // 100_000

    def inner(number: int, magnitude: int, streak: int, has_pair: bool):
        next_magnitude = magnitude * 10
        last_digit = number // magnitude

        if next_magnitude == 100_000:
            for digit in range(start_top, min(stop_top, last_digit) + 1):
                num = number + digit * next_magnitude
                if not start <= num <= stop:
                    continue
                # Test if the last 2 digits are a strict pair
                if has_pair or streak == 1 + (digit != last_digit):
                    yield num

        else:
            for digit in range(start_top, last_digit + 1):
                num = number + digit * next_magnitude
                if digit == last_digit:
                    yield from inner(num, next_magnitude, streak + 1, has_pair)
                else:
                    yield from inner(num, next_magnitude, 1, has_pair or streak == 2)

    return sum(True for i in range(10) for _ in inner(i, 1, 1, False))


def main(data: str):
    start, stop = map(int, data.strip().split("-"))
    assert 100_000 <= start < 1_000_000
    assert 100_000 <= stop < 1_000_000
    yield part_1(start, stop)
    yield part_2(start, stop)
