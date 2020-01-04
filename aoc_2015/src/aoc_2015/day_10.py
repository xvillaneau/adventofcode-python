"""
Advent of Code 2015, day 10
https://adventofcode.com/2015/day/10

== The "Look and Say" sequence ==

I solved it for fun ahead of AoC 2019, and was dragged into weeks of
research on this problem alone. It's FASCINATING.

The simplest approach to solving this is to write the Look-and-Say
transformation, then apply it many times. Problem is: the length of its
output grows exponentially! Consequently, a naive implementation might
run 40 iterations without trouble but see its run time soar for 50
iterations. And don't even think about doing 60 or 70.

Maybe it's because I solved it in 2019, but part 2 (50 iterations) was
not too difficult to brute-force with my laptop. I knew I could do
better though. That's where John Conway's research comes in.

This solution is based on two of his findings:
 1. The Splitting Theorem, which states that strings can be split in
    such a way that both sides never interact ever again,
 2. The Chemical Theorem, which states that after enough iterations
    (24 at most) ALL strings can eventually be expressed as compounds
    of a finite set of 92 (+2) elements.

With this, I designed a recursive cached solution that:
 *  Computes the length of a string's descendents by splitting it
    then recursively computing the length of each compound,
 *  Caches enough of those results so that the recursion terminates
    early under the correct conditions.

This solution runs in roughly O(n.log(n)). Doing 50 iterations takes
around 2 milliseconds on my machine. It can even calculate the length
of the 10,000th term under a second. Try it out!
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

    @lru_cache(maxsize=2048)
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
