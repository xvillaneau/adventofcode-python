from math import log10
from typing import List
import re

RE_PART_1 = re.compile(r'(.)\1')
RE_PART_2 = re.compile(r'(.)(?<!\1.)\1(?!\1)')


def acceptable_passwords(start: int, end: int, re_check):

    start = tuple(map(int, str(start)))
    end = tuple(map(int, str(end)))
    assert len(start) == len(end)
    depth = len(start)

    def _rec_passwords(stack):
        if len(stack) == depth:
            full_pw = ''.join(map(str, stack))
            yield bool(re_check.search(full_pw))
            return
        prev = stack[-1] if stack else 0
        zeros = (0,) * (depth - len(stack) - 1)
        nines = (9,) * len(zeros)
        for digit in range(prev, 10):
            _nxt = stack + (digit,)
            if _nxt + nines < start:
                continue
            if _nxt + zeros > end:
                break
            yield from _rec_passwords(_nxt)

    yield from _rec_passwords(())

def part_1(numbers):
    return sum(acceptable_passwords(*numbers, RE_PART_1))

def part_2(numbers):
    return sum(acceptable_passwords(*numbers, RE_PART_2))


if __name__ == '__main__':
    from libaoc import simple_main, static_input
    simple_main(2019, 4, static_input((138241, 674034)), part_1, part_2)
