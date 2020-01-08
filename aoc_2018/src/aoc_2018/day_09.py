
from collections import deque
import re
from libaoc import tuple_main, files


class Game:

    __slots__ = ['marbles', 'scores', 'current_value', 'next_scorer']

    def __init__(self, n_players: int):
        self.marbles = deque([0])
        self.scores = [0] * n_players
        self.current_value = 1
        self.next_scorer = 23 % n_players

    def round(self):
        for i in range(22):
            self.marbles.rotate(-2)
            self.marbles.appendleft(self.current_value + i)
        self.marbles.rotate(7)
        self.scores[self.next_scorer] += self.marbles.popleft() + self.current_value + 22
        self.next_scorer = (self.next_scorer + 23) % len(self.scores)
        self.current_value += 23

    def play(self, max_value: int):
        while self.current_value <= max_value:
            self.round()


def main(game_input: str):
    # Parse the puzzle input
    match = re.search(r'(\d+) players; last marble is worth (\d+) points', game_input)
    players, max_val = map(int, match.groups())
    # Run game for first rounf
    g = Game(players)
    g.play(max_val)
    score_1 = max(g.scores)
    # Second run!
    g.play(max_val * 100)
    return score_1, max(g.scores)


if __name__ == '__main__':
    tuple_main(2018, 9, files.read_full, main)
