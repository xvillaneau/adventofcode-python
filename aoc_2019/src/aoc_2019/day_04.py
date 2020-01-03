def part_1(start: int, stop: int):
    start_top, stop_top = start // 100_000, stop // 100_000

    def _password_gen(number: int, magnitude: int, has_pair: bool):
        next_magnitude = magnitude * 10
        last_digit = number // magnitude

        if next_magnitude == 100_000:
            for digit in range(start_top, min(stop_top, last_digit) + 1):
                num = number + digit * next_magnitude
                if (has_pair or digit == last_digit) and start <= num <= stop:
                    yield num

        else:
            for digit in range(last_digit + 1):
                num = number + digit * next_magnitude
                double = has_pair or digit == last_digit
                yield from _password_gen(num, next_magnitude, double)

    return sum(True for i in range(10) for _ in _password_gen(i, 1, False))


def part_2(start: int, stop: int):
    start_top, stop_top = start // 100_000, stop // 100_000

    def _password_gen(number: int, magnitude: int, streak: int, has_pair: bool):
        next_magnitude = magnitude * 10
        last_digit = number // magnitude

        if next_magnitude == 100_000:
            for digit in range(start_top, min(stop_top, last_digit) + 1):
                num = number + digit * next_magnitude
                repeat = 1 if digit != last_digit else streak + 1
                good = has_pair or repeat == 2 or (repeat == 1 and streak == 2)
                if start <= num <= stop and good:
                    yield num

        else:
            for digit in range(last_digit + 1):
                num = number + digit * next_magnitude
                repeat = 1 if digit != last_digit else streak + 1
                good = has_pair or (repeat == 1 and streak == 2)
                yield from _password_gen(num, next_magnitude, repeat, good)

    return sum(True for i in range(10) for _ in _password_gen(i, 1, 1, False))


def main(data: str):
    start, stop = map(int, data.strip().split("-"))
    assert 100_000 <= start < 1_000_000
    assert 100_000 <= stop < 1_000_000
    yield part_1(start, stop)
    yield part_2(start, stop)
