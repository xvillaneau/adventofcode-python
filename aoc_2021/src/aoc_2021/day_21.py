from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import product


def parse_start_pos(data: str) -> tuple[int, int]:
    p1, _, p2 = data.strip().partition("\n")
    p1 = int(p1.partition(": ")[2])
    p2 = int(p2.partition(": ")[2])
    return p1, p2


def practice_game(p1: int, p2: int) -> int:

    @dataclass
    class Player:
        pos: int
        score: int = 0

    dice, rolls = 1, 0

    def move(player: Player):
        nonlocal dice, rolls
        rolls += 3
        player.pos = 1 + (player.pos + dice * 3 + 2) % 10
        dice = 1 + (dice + 2) % 100
        player.score += player.pos
        return player.score

    p1, p2 = Player(p1), Player(p2)
    while True:
        if move(p1) >= 1000:
            return p2.score * rolls
        if move(p2) >= 1000:
            return p1.score * rolls


# Instead of simulating all 3 rolls every time,
# pre-compute the possible outputs of 3 consecutive rolls.
# That way we only need 7 iterations per round instead of 27.
DIRAC_3_ROLLS = Counter(sum(p) for p in product((1, 2, 3), repeat=3))


def dirac_game(p1: int, p2: int, win=21):

    # Cache results for 500x speedup!
    @lru_cache(maxsize=None)
    def game_step(
        p1_pos: int,
        p2_pos: int,
        p1_score: int = 0,
        p2_score: int = 0,
        p1s_turn: bool = True,
    ):
        if p1_score >= win:
            return 1, 0
        elif p2_score >= win:
            return 0, 1

        p1_wins, p2_wins = 0, 0
        for roll, count in DIRAC_3_ROLLS.items():
            if p1s_turn:
                w1, w2 = game_step(
                    (n_pos := 1 + (p1_pos + roll - 1) % 10),
                    p2_pos,
                    p1_score + n_pos,
                    p2_score,
                    False,
                )
            else:
                w1, w2 = game_step(
                    p1_pos,
                    (n_pos := 1 + (p2_pos + roll - 1) % 10),
                    p1_score,
                    p2_score + n_pos,
                    True,
                )

            p1_wins += w1 * count
            p2_wins += w2 * count

        return p1_wins, p2_wins

    return game_step(p1, p2)


def main(data: str):
    p1, p2 = parse_start_pos(data)
    yield practice_game(p1, p2)
    yield max(dirac_game(p1, p2))
