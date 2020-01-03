def to_digits(number):
    digits = []
    while number:
        digits.append(number % 10)
        number //= 10
    return digits[::-1]


def test_password(number):
    digits = to_digits(number)
    has_pair = False

    previous = digits[0]
    for digit in digits[1:]:
        if digit < previous:
            return False
        if digit == previous:
            has_pair = True
        previous = digit

    return has_pair


def test_password_2(number):
    digits = to_digits(number)
    has_good_pair = False
    streak = 1

    previous = digits[0]
    for digit in digits[1:]:
        if digit < previous:
            return False
        elif digit == previous:
            streak += 1
        else:  # digit > previous
            if streak == 2:
                has_good_pair = True
            streak = 1
        previous = digit

    if streak == 2:
        has_good_pair = True

    return has_good_pair


def parse_input_range(data: str):
    """Convert the input string into start and stop values"""
    start, _, stop = data.partition("-")
    return int(start), int(stop)


def part_1(start, stop):
    """Part 1 of AoC 2019, day 4"""
    return sum(test_password(num) for num in range(start, stop + 1))


def part_2(start, stop):
    """Part 2 of AoC 2019, day 4"""
    return sum(test_password_2(num) for num in range(start, stop + 1))


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
