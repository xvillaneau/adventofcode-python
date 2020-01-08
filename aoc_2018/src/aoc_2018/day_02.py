
from itertools import combinations
from collections import Counter


def count_checks(words):
    counters = [Counter(w) for w in words]
    check2 = sum(2 in c.values() for c in counters)
    check3 = sum(3 in c.values() for c in counters)
    return check2 * check3


def diff_words(w1, w2):
    return sum(a != b for a, b in zip(w1, w2))


def find_closest(words):
    return next(t for t in combinations(words, 2) if diff_words(*t) == 1)


def main(data):
    words = data.splitlines()
    yield count_checks(words)
    yield find_closest(words)
