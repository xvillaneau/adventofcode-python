import functools
from collections import Counter

ORDER_1 = "23456789TJQKA"
ORDER_2 = "J23456789TQKA"
TYPES: dict[tuple[int, ...], int] = {
    (5,): 7,
    (1, 4): 6,
    (2, 3): 5,
    (1, 1, 3): 4,
    (1, 2, 2): 3,
    (1, 1, 1, 2): 2,
    (1, 1, 1, 1, 1): 1,
}


@functools.lru_cache(maxsize=None)
def hand_order(hand: str) -> tuple[int, ...]:
    counts = Counter(hand)
    count_type = tuple(sorted(counts.values()))
    return TYPES.get(count_type, 0), *(ORDER_1.index(c) for c in hand)


@functools.lru_cache(maxsize=None)
def hand_joker_order(hand: str) -> tuple[int, ...]:
    counts = Counter(hand)
    if "J" in counts and len(counts) > 1:
        n_joker = counts.pop("J")
        add_to = max(counts.keys(), key=counts.get)
        counts[add_to] += n_joker
    count_type = tuple(sorted(counts.values()))
    return TYPES.get(count_type, 0), *(ORDER_2.index(c) for c in hand)


def main(data: str):
    hands = [
        (line[:5], int(line[6:]))
        for line in data.splitlines()
    ]

    part_1 = sorted(hands, key=lambda x: hand_order(x[0]))
    yield sum(bid * i for i, (_, bid) in enumerate(part_1, start=1))

    part_2 = sorted(hands, key=lambda x: hand_joker_order(x[0]))
    yield sum(bid * i for i, (_, bid) in enumerate(part_2, start=1))
