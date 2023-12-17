import re


def parse_cards(lines: list[str]) -> dict[int, int]:
    cards = {}
    for ln in lines:
        m = re.fullmatch(r"Card +(\d+): ([\d ]+) \| ([\d ]+)", ln)
        card, wins_str, nums_str = m.groups()
        wins = frozenset(int(n) for n in wins_str.split())
        nums = frozenset(int(n) for n in nums_str.split())
        cards[int(card)] = len(wins & nums)
    return cards


def score(matches: int):
    if matches == 0:
        return 0
    return 1 << (matches - 1)


def card_game(cards: dict[int, int]):
    cache = {}

    def count_cards(card: int):
        if card in cache:
            return cache[card]
        count = 1  # This card
        # Iterate in reverse order so that we hopefully populate the cache
        # for the higher cards in fewer calls.
        for i in range(cards[card], 0, -1):
            count += count_cards(card + i)
        cache[card] = count
        return count

    return sum(count_cards(c) for c in cards.keys())


def main(data: str):
    cards = parse_cards(data.strip().splitlines())
    yield sum(score(m) for m in cards.values())
    yield card_game(cards)
