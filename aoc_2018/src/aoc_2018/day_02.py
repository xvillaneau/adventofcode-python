
from itertools import combinations
from collections import Counter
from libaoc import files, simple_main


def count_checks(words):
    counters = [Counter(w) for w in words]
    check2 = sum(2 in c.values() for c in counters)
    check3 = sum(3 in c.values() for c in counters)
    return check2 * check3


def diff_words(w1, w2):
    return sum(a != b for a, b in zip(w1, w2))


def find_closest(words):
    return next(t for t in combinations(words, 2) if diff_words(*t) == 1)


if __name__ == '__main__':
    simple_main(2018, 2, files.read_lines, count_checks, find_closest)
