from collections import deque, Iterable

Deck = deque[int]
TDeck = tuple[int, ...]


def parse_deck(data: str) -> tuple[Deck, Deck]:
    _, p1, p2 = data.split('Player')
    d1 = p1.partition(':')[2].strip().splitlines()
    d2 = p2.partition(':')[2].strip().splitlines()
    return deque(map(int, d1)), deque(map(int, d2))


def play_round(deck_1: Deck, deck_2: Deck):
    c1, c2 = deck_1.popleft(), deck_2.popleft()
    if c1 > c2:
        deck_1.append(c1)
        deck_1.append(c2)
    else:
        deck_2.append(c2)
        deck_2.append(c1)


def play_game(deck_1: Deck, deck_2: Deck) -> Deck:
    while deck_1 and deck_2:
        play_round(deck_1, deck_2)
    return deck_1 or deck_2


def play_recursive_round(deck_1: TDeck, deck_2: TDeck):
    c1, c2 = deck_1[0], deck_2[0]
    deck_1, deck_2 = deck_1[1:], deck_2[1:]
    if len(deck_1) >= c1 and len(deck_2) >= c2:
        p1_wins, _ = play_recursive_game(deck_1[:c1], deck_2[:c2])
    else:
        p1_wins = c1 > c2
    if p1_wins:
        return deck_1 + (c1, c2), deck_2
    else:
        return deck_1, deck_2 + (c2, c1)


def play_recursive_game(deck_1: TDeck, deck_2: TDeck) -> tuple[bool, TDeck]:
    rounds = set()
    while deck_1 and deck_2:
        if (deck_1, deck_2) in rounds:
            p1_wins = True
            break
        rounds.add((deck_1, deck_2))
        deck_1, deck_2 = play_recursive_round(deck_1, deck_2)
    else:
        p1_wins = bool(deck_1)

    return p1_wins, deck_1 if p1_wins else deck_2


def score(deck: Iterable[int]) -> int:
    return sum(n * i for i, n in enumerate(reversed(deck), start=1))


def main(data: str):
    deck_1, deck_2 = parse_deck(data)
    yield score(play_game(deck_1, deck_2))

    deck_1, deck_2 = parse_deck(data)
    _, winner = play_recursive_game(tuple(deck_1), tuple(deck_2))
    yield score(winner)
