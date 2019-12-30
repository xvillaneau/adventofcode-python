import re
from typing import Tuple

from libaoc import BaseRunner


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


class AocRunner(BaseRunner):
    year = 2019
    day = 4

    @staticmethod
    def parser(data: str):
        a, b = data.strip().split('-')
        return int(a), int(b)

    def run(self, data: Tuple[int, int]):
        start, stop = data
        yield sum(acceptable_passwords(start, stop, RE_PART_1))
        yield sum(acceptable_passwords(start, stop, RE_PART_2))
