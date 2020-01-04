"""
Advent of Code 2015, day 10
https://adventofcode.com/2015/day/10

Run it with:  python run_aoc.py 2015 10
Read the docs at:  /aoc_2015/docs/day_10.md
"""
from functools import lru_cache
from itertools import count, groupby, islice
import re
from typing import List, Generator


def look_and_say(string: str):
    """Alternate look-and-say implementation using itertools"""
    result = ""
    for char, grouper in groupby(string):
        result += str(sum(1 for _ in grouper)) + char
    return result


# Splitting a sequence
RE_END_SPLIT = re.compile(r"[^2]22$")
RE_SPLITS = [
    re.compile(r"21([^1])(?!\1)"),
    re.compile(r"2111[^1]"),
    re.compile(r"23(?:$|([^3]){1,2}(?!\1))"),
    re.compile(r"2([^123])(?!\1)"),
    re.compile(r"[^123][123]"),
]


def split(string: str) -> List[str]:
    """
    Split a string, as described in Conway's Splitting Theorem.
    IMPORTANT: DO NOT APPLY TO zero-day or one-day strings!
    """
    return list(_split(string))


def _split(string: str) -> Generator[str, None, None]:
    """Internal recursive generator for splitting"""
    if RE_END_SPLIT.search(string):
        yield from _split(string[:-2])
        yield "22"
    else:
        for regex in RE_SPLITS:
            match = regex.search(string)
            if match:
                p = match.start() + 1
                yield from _split(string[:p])
                yield from _split(string[p:])
                return
        # No matches
        yield string


@lru_cache(maxsize=128)
def memoized_look_say_split(string: str) -> List[str]:
    """
    Runs look-and-say then splits the result.
    IMPORTANT: DO NOT APPLY TO zero-day strings!
    """
    return split(look_and_say(string))


def iter_look_and_say_lengths(string: str) -> Generator[int, None, None]:
    """
    Iterate over the lengths of the consecutive look-and-say
    applications, starting with the given string.
    """

    @lru_cache(maxsize=4096)
    def recursive_lns_length(_string: str, depth: int) -> int:
        """
        This function MUST be called with incremental depths otherwise
        it will miss the cache and recurse pass the stack size. Hence
        why it's hidden in the closure of the iterator.
        """
        if depth <= 0:
            return len(_string)
        res, n_depth = 0, depth - 1
        for atom in memoized_look_say_split(_string):
            res += recursive_lns_length(atom, n_depth)
        return res

    yield len(string)
    string = look_and_say(string)
    for i in count():
        yield recursive_lns_length(string, i)


def main(string: str):
    """Yields the lengths at 40 and 50 steps"""
    iterator = iter_look_and_say_lengths(string)
    yield next(islice(iterator, 40, None))
    yield next(islice(iterator, 9, None))
