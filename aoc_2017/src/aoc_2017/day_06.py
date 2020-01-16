from typing import List

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


def count_cycles(bank: Bank):

    mem = bank.copy()
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


if __name__ == '__main__':
    from libaoc import iter_main, files
    iter_main(2017, 6, files.read_int_list, count_cycles)
