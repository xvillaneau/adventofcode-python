from typing import List

from libaoc.parsers import parse_integer_list

Bank = List[int]


def pick_index(bank: Bank) -> int:
    max_bank = max(bank)
    candidates = set(i for i, x in enumerate(bank) if x == max_bank)
    return min(candidates)


def rebalance(bank: Bank) -> Bank:
    pick, n = pick_index(bank), len(bank)
    quo, rem = divmod(bank[pick], n)
    moves = [quo + 1] * rem + [quo] * (n - rem)
    return [
        (0 if i == pick else x) + moves[(i - pick - 1) % n]
        for i, x in enumerate(bank)]


def main(data: str):

    mem = parse_integer_list(data)
    states = set([])
    cycles = 0

    while True:
        if tuple(mem) in states:
            yield cycles
            states = set([])
            cycles = 0
        states.add(tuple(mem))
        mem = rebalance(mem)
        cycles += 1
