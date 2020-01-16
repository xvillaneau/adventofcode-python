from typing import List, Tuple


def int_to_digits(number: int) -> List[int]:
    out = []
    while number >= 10:
        out.append(number % 10)
        number = number // 10
    out.append(number)
    return list(reversed(out))


def digits_to_couples(digits: List[int], offset: int=-1) -> List[Tuple[int, int]]:
    return list(zip(digits, digits[offset:] + digits[:offset]))


def sum_couples(couples: List[Tuple[int, int]]):
    return sum(a for a, b in couples if a == b)


def captcha(number: int):
    return sum_couples(digits_to_couples(int_to_digits(number)))


def captcha_2(number: int):
    digits = int_to_digits(number)
    assert len(digits) % 2 == 0
    return sum_couples(digits_to_couples(digits, len(digits) // 2))


def main(data: str):
    number = int(data)
    yield captcha(number)
    yield captcha_2(number)
