from functools import lru_cache, reduce
from math import prod
from typing import List, Tuple

from more_itertools import windowed


def prepare_data(adapters: List[int]) -> None:
    adapters.sort()
    adapters.insert(0, 0)
    adapters.append(adapters[-1] + 3)


def count_deltas(adapters: List[int]) -> Tuple[int, int]:
    def reduce_count(acc, value):
        diff = value[1] - value[0]
        return acc[0] + (diff == 1), acc[1] + (diff == 3)

    return reduce(reduce_count, windowed(adapters, 2), (0, 0))


def count_arrangements(adapters: List[int]) -> int:

    @lru_cache(maxsize=None)
    def _arrangements_at(index: int):
        if index == len(adapters) - 1:
            return 1

        jolts, *next_jolts = adapters[index:index + 4]
        return sum(
            _arrangements_at(i)
            for i, n in enumerate(next_jolts, start=index + 1)
            if n <= jolts + 3
        )

    return _arrangements_at(0)


def main(data: str):
    adapters = [int(n) for n in data.splitlines()]
    prepare_data(adapters)
    yield prod(count_deltas(adapters))
    yield count_arrangements(adapters)
