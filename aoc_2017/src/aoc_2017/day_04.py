from itertools import permutations, combinations
from typing import List


def is_anagram(word1, word2):
    return any(''.join(letters) == word1
               for letters in permutations(word2))


def has_no_anagrams(phrase):
    if not has_no_duplicates(phrase):
        return False
    words = phrase.split()
    return not any(is_anagram(w1, w2) for w1, w2 in combinations(words, 2))


def has_no_duplicates(phrase: str) -> bool:
    if not phrase:
        return False
    words = phrase.split()
    return len(words) == len(set(words))


def day_04(phrases: List[str]):
    yield sum(has_no_duplicates(p) for p in phrases)
    yield sum(has_no_anagrams(p) for p in phrases)


if __name__ == '__main__':
    from libaoc import iter_main, files
    iter_main(2017, 4, files.read_lines, day_04)
