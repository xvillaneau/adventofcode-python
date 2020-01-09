import re

RE_FORBIDDEN = re.compile(r'ab|cd|pq|xy')
RE_VOWELS = re.compile(r'[aeiou]')
RE_DOUBLES = re.compile(r'(.)\1')


def is_nice(string: str):
    return (
        RE_FORBIDDEN.search(string) is None
        and RE_DOUBLES.search(string) is not None
        and len(RE_VOWELS.findall(string)) >= 3
    )


RE_DISTINCT_PAIRS = re.compile(r'(..).*\1')
RE_REPEAT_SPACED = re.compile(r'(.).\1')


def is_nicer(string):
    return (
        RE_REPEAT_SPACED.search(string) is not None
        and RE_DISTINCT_PAIRS.search(string) is not None
    )


def main(data: str):
    strings = data.splitlines()
    nice, nicer = 0, 0
    for s in strings:
        nice += is_nice(s)
        nicer += is_nicer(s)
    yield nice
    yield nicer
