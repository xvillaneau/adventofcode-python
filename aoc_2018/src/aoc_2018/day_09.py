from collections import deque
import re


class Game:
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
        self.scores[self.next_scorer] += (
            self.marbles.popleft() + self.current_value + 22
        )
        self.next_scorer = (self.next_scorer + 23) % len(self.scores)
        self.current_value += 23

    def play(self, max_value: int):
        while self.current_value <= max_value:
            self.round()


def main(game_input: str):
    # Parse the puzzle input
    match = re.search(r"(\d+) players; last marble is worth (\d+) points", game_input)
    players, max_val = int(match.group(1)), int(match.group(2))
    # Run game for first round
    g = Game(players)
    g.play(max_val)
    yield max(g.scores)
    # Second run!
    g.play(max_val * 100)
    yield max(g.scores)
