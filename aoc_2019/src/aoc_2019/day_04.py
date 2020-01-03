def part_1(start: int, stop: int):
    assert 100_000 <= start <= 999_999
    assert 100_000 <= stop <= 999_999

    start_top, stop_top = start // 100_000, stop // 100_000

    def _password_gen(number: int, magnitude: int, last_digit: int, has_double: bool):
        if magnitude == 100_000:
            for digit in range(start_top, min(stop_top, last_digit) + 1):
                num = number + digit * magnitude
                if (has_double or digit == last_digit) and start <= num <= stop:
                    yield num
        else:
            next_magnitude = magnitude * 10
            for digit in range(last_digit + 1):
                num = number + digit * magnitude
                double = has_double or digit == last_digit
                yield from _password_gen(num, next_magnitude, digit, double)

    return sum(True for i in range(10) for _ in _password_gen(i, 10, i, False))


def part_2(start: int, stop: int):
    assert 100_000 <= start <= 999_999
    assert 100_000 <= stop <= 999_999

    start_top, stop_top = start // 100_000, stop // 100_000

    def _password_gen(
        number: int, magnitude: int, last_digit: int, streak: int, has_good_double: bool
    ):
        if magnitude == 100_000:
            for digit in range(start_top, min(stop_top, last_digit) + 1):
                num = number + digit * magnitude
                repeat = 1 if digit != last_digit else streak + 1
                if start <= num <= stop and (
                    has_good_double or repeat == 2 or repeat == 1 and streak == 2
                ):
                    yield num

        else:
            next_magnitude = magnitude * 10
            for digit in range(last_digit + 1):
                num = number + digit * magnitude
                repeat = 1 if digit != last_digit else streak + 1
                good = has_good_double or (repeat == 1 and streak == 2)
                yield from _password_gen(num, next_magnitude, digit, repeat, good)

    return sum(True for i in range(10) for _ in _password_gen(i, 10, i, 1, False))


def main(data: str):
    start, stop = map(int, data.strip().split("-"))
    yield part_1(start, stop)
    yield part_2(start, stop)
