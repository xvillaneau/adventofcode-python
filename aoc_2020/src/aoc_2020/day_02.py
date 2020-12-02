import re


def password_valid_1(letter: str, low: int, high: int, password: str):
    return low <= password.count(letter) <= high


def password_valid_2(letter, pos_1, pos_2, password):
    let_1, let_2 = password[pos_1 - 1], password[pos_2 - 1]
    return (let_1 == letter) != (let_2 == letter)


RE_LINE = re.compile(r'(\d+)-(\d+) ([a-z]): ([a-z]+)')


def parse_line(line: str):
    low, high, letter, password = RE_LINE.fullmatch(line).groups()
    return letter, int(low), int(high), password


def main(data: str):
    count_1, count_2 = 0, 0
    for line in data.splitlines():
        line_data = parse_line(line)
        count_1 += password_valid_1(*line_data)
        count_2 += password_valid_2(*line_data)
    yield count_1
    yield count_2
