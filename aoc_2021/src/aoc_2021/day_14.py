from collections import Counter
from functools import lru_cache

from more_itertools import windowed


def parse_data(data: str) -> tuple[str, dict[str, str]]:
    template, _, s_pairs = data.strip().partition("\n\n")
    pairs = {}
    for line in s_pairs.splitlines():
        pair, _, insert = line.partition(" -> ")
        pairs[pair] = insert
    return template, pairs


def polymer_delta(template: str, pairs: dict[str, str], steps: int) -> int:

    @lru_cache(maxsize=2048)
    def pair_counts(pair: str, depth: int) -> Counter:
        if depth == 0:
            return Counter(pair)
        a, c = pair
        b = pairs[pair]
        cnt = pair_counts(a + b, depth - 1) + pair_counts(b + c, depth - 1)
        cnt[b] -= 1
        return cnt

    tmpl_pairs = [a + b for a, b in windowed(template, 2)]
    counts = Counter()
    for n in range(steps):
        # Iterating over depths makes the cache "roll",
        # allow for constant(-ish) memory use at any depth.
        # This still works at depths of 10000 or more!
        counts = sum((pair_counts(p, n + 1) for p in tmpl_pairs), Counter())
    counts -= Counter(template[1:-1])

    return max(counts.values()) - min(counts.values())


def main(data: str):
    polymer, pairs = parse_data(data)
    yield polymer_delta(polymer, pairs, 10)
    yield polymer_delta(polymer, pairs, 40)
