
from collections import Counter
import re
from libaoc import files, simple_main

RE_LINE = re.compile(r'^([a-z-]+)-([0-9]+)\[([a-z]+)\]$')


def parse_line(line: str):
    match = RE_LINE.match(line)
    number = int(match.groups()[1])
    return match.groups()[0], number, match.groups()[2]


def checksum(name: str):

    def _count_key(t):
        l, c = t
        return c, -ord(l)

    counts = sorted(Counter(name.replace('-', '')).most_common(), key=_count_key, reverse=True)
    return ''.join(x for x, _ in counts[:5])


def real_rooms(lines):
    rooms = map(parse_line, lines)
    return iter((name, nb) for name, nb, ck in rooms if checksum(name) == ck)


def shift(name: str, num: int):

    def _shift(char):
        if char == '-':
            return " "
        return chr(97 + (ord(char) - 97 + num) % 26)

    return ''.join(map(_shift, name))


def sum_score(lines):
    return sum(n for _, n in real_rooms(lines))


def decrypt_names(lines):
    rooms = [(shift(name, nb), nb) for name, nb in real_rooms(lines)]
    return [(n, i) for n, i in rooms if 'north' in n]


if __name__ == '__main__':
    simple_main(2016, 4, files.read_lines, sum_score, decrypt_names)
