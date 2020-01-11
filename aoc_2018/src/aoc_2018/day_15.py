from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Tuple, List

import numpy as np
from scipy import ndimage

from libaoc.matrix import load_string_matrix

Pos = Tuple[int, int]
ELF, GOBLIN = "elf", "goblin"


@dataclass
class Player:
    x: int
    y: int
    clan: str
    attack: int = 3
    health: int = 200

    @property
    def pos(self):
        return self.x, self.y

    def move(self, pos: Pos):
        self.x, self.y = pos


class Game:
    def __init__(self, map_str, elf_atk=3):
        chars_mat = load_string_matrix(map_str)
        self.playable = chars_mat != '#'
        self.rounds = 0

        elves = [Player(x, y, ELF, elf_atk) for x, y in np.argwhere(chars_mat == 'E')]
        goblins = [Player(x, y, GOBLIN) for x, y in np.argwhere(chars_mat == 'G')]
        self.players = elves + goblins
        self._goblin_id = len(elves)
        self._n_elves, self._n_goblins = len(elves), len(goblins)

    @property
    def elves(self):
        return [p for p in self.players[:self._goblin_id] if p.health > 0]

    @property
    def goblins(self):
        return [p for p in self.players[self._goblin_id:] if p.health > 0]

    @property
    def score(self):
        return self.rounds * sum(p.health for p in self.players if p.health > 0)

    @property
    def ordered_players(self):
        players = self.players
        ids = range(len(players))
        ids = sorted(ids, key=lambda i: players[i].pos)
        return list(ids)

    @property
    def complete(self):
        return self._n_elves == 0 or self._n_goblins == 0

    def elves_mat(self):
        return player_map(self.playable.shape, self.elves)

    def goblins_mat(self):
        return player_map(self.playable.shape, self.goblins)

    def show_state(self, health=False):
        indices = ~self.playable * 1 + self.elves_mat() * 2 + self.goblins_mat() * 3
        full_map = np.choose(indices, ('.', '#', 'E', 'G'))
        if not health:
            lines = (''.join(line) for line in full_map)
        else:
            lines = []
            for x, line in enumerate(full_map):
                line = "".join(line)
                on_line = [p for p in self.players if p.x == x]
                on_line.sort(key=lambda p: p.y)
                players = ", ".join(
                    f"{p.clan[0].upper()}({p.health})"
                    for p in on_line
                    if p.health > 0
                )
                lines.append(line + "   " + players)
        return "\n".join(lines)

    def __str__(self):
        """Generate a fancy visualization of how the battle is doing"""
        return self.show_state()

    def next_move(self, player_id: int):
        player = self.players[player_id]
        if player.health <= 0:
            return player.pos

        goblins, elves = self.goblins_mat(), self.elves_mat()
        enemies = goblins if player.clan == ELF else elves

        start_pos = player.pos
        attack_ranges = ndimage.binary_dilation(enemies)
        if attack_ranges[start_pos]:
            return start_pos

        free = self.playable & ~goblins & ~elves
        frontier, visited = [], set()
        for first_step in neighbors(start_pos):
            if not free[first_step]:
                continue
            heappush(frontier, (1, first_step, first_step))
            visited.add(first_step)

        while frontier:
            steps, first_pos, pos = heappop(frontier)
            if attack_ranges[pos]:
                return first_pos
            for next_pos in neighbors(pos):
                if next_pos in visited or not free[next_pos]:
                    continue
                visited.add(next_pos)
                heappush(frontier, (steps + 1, first_pos, next_pos))

        return start_pos

    def play_turn(self, player_id: int, allow_elf_death=True):
        player = self.players[player_id]
        next_move = self.next_move(player_id)

        player.move(next_move)

        enemies = self.goblins if player.clan == ELF else self.elves
        adjacent_pos = set(neighbors(player.pos))

        targets = [p for p in enemies if p.pos in adjacent_pos]
        if not targets:
            return True

        target = min(targets, key=lambda p: (p.health, p.pos))
        target.health -= player.attack

        if target.health <= 0:  # Target down
            if target.clan == ELF:
                if not allow_elf_death:
                    return False
                self._n_elves -= 1
            else:
                self._n_goblins -= 1

        return True

    def play(self, allow_elf_death=True):
        while True:
            round_order = self.ordered_players
            for player_id in round_order:
                if self.complete:
                    return
                if self.players[player_id].health <= 0:
                    continue
                self.play_turn(player_id, allow_elf_death)
            self.rounds += 1


def player_map(shape, players: List[Player]):
    pos_ind = np.array([p.pos for p in players]).transpose()
    if not np.any(pos_ind):
        return np.full(shape, False)
    int_ind = np.ravel_multi_index(pos_ind, shape)
    np.put(mat := np.full(shape, False), int_ind, True)
    return mat


def neighbors(pos: Tuple[int, int]):
    x, y = pos
    yield x-1, y
    yield x, y-1
    yield x, y+1
    yield x+1, y


def main(data: str):
    game = Game(data)
    game.play()
    yield game.score
