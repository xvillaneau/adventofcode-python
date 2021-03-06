from collections import Counter
from typing import List


def letter_counters(words: List[str]):
    counters = [Counter() for _ in words[0]]
    for word in words:
        for i, c in enumerate(word):
            counters[i].update(c)
    return counters


def repeated_letters(words):
    counters = letter_counters(words)
    return "".join(c.most_common(1)[0][0] for c in counters)


def least_common_letters(words):
    def _least_common(c: Counter):
        ls = sorted(c.most_common(), key=lambda t: t[1])
        return ls[0][0]

    return "".join(_least_common(c) for c in letter_counters(words))


def main(data: str):
    lines = data.splitlines()
    yield repeated_letters(lines)
    yield least_common_letters(lines)
