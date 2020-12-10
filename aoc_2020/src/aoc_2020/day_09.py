from collections import defaultdict
from typing import List

from more_itertools import windowed


def find_invalid(message: List[int], buffer=25) -> int:
    tail = 0
    sums = defaultdict(int)

    for head, num in enumerate(message):
        if head - tail == buffer:
            if not sums[num]:
                return num

            removed = message[tail]
            for n in message[tail + 1:head]:
                sums[removed + n] -= 1
            tail += 1

        for n in message[tail:head]:
            sums[num + n] += 1

    return -1


def find_weakness(message: List[int], invalid_num: int) -> int:

    def _weakness(size, start, end):
        if end - start < size:
            return None

        windows = windowed(message[start:end], size)
        for k, window in enumerate(windows, start=start):
            window_sum = sum(window)
            if window_sum == invalid_num:
                return min(window) + max(window)
            elif window_sum > invalid_num:
                if (res := _weakness(size + 1, start, k + size - 1)):
                    return res
                start = k + 1

        return _weakness(size + 1, start, end)

    return _weakness(2, 0, len(message))


def main(data: str):
    message = list(map(int, data.splitlines()))
    yield (invalid_num := find_invalid(message))
    yield find_weakness(message, invalid_num)
