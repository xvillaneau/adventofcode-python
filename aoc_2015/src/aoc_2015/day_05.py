import re

FORBIDDEN = re.compile(r'ab|cd|pq|xy')
VOWELS = re.compile(r'[aeiou].*[aeiou].*[aeiou]')
DOUBLES = re.compile(r'(.)\1')

def is_nice(string: str):
    if FORBIDDEN.search(string):
        return False
    return bool(VOWELS.search(string) and DOUBLES.search(string))

def test_is_nice():
    assert is_nice("ugknbfddgicrmopn")
    assert is_nice("aaa")
    assert not is_nice("jchzalrnumimnmhp")
    assert not is_nice("haegwjzuvuyypxyu")
    assert not is_nice("dvszwmarrgswjxmb")

RULE_1 = re.compile(r'(..).*\1')
RULE_2 = re.compile(r'(.).\1')

def is_nicer(string):
    return bool(RULE_1.search(string) and RULE_2.search(string))

def test_is_nicer():
    assert is_nicer("qjhvhtzxzqqjkmpb")
    assert is_nicer("xxyxx")
    assert not is_nicer("uurcxstgmygtbstg")
    assert not is_nicer("ieodomkazucvgmuy")

def nice_counts(strings):
    nice, nicer = 0, 0
    for s in strings:
        nice += is_nice(s)
        nicer += is_nicer(s)
    return nice, nicer


def main(data: str):
    yield from nice_counts(data.splitlines())
