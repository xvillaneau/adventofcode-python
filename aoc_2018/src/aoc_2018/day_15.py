from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Tuple
from functools import lru_cache

import numpy as np

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
        self.playable: np.ndarray = chars_mat != '#'
        self.rounds = 0

        elves = [Player(x, y, ELF, elf_atk) for x, y in np.argwhere(chars_mat == 'E')]
        goblins = [Player(x, y, GOBLIN) for x, y in np.argwhere(chars_mat == 'G')]
        self.players = elves + goblins
        self._clans_pivot = len(elves)

        self.elves, self.goblins = elves, goblins
        # Cached values
        self._n_elves, self._n_goblins = len(elves), len(goblins)
        self._elf_ranges, self._goblin_ranges = set(), set()
        self._elves_pos, self._goblins_pos = set(), set()
        self._refresh_elves()
        self._refresh_goblins()

    def _kill_elf(self, elf: Player):
        self._n_elves -= 1
        self.elves.remove(elf)
        self._refresh_elves()

    def _kill_goblin(self, goblin: Player):
        self._n_goblins -= 1
        self.goblins.remove(goblin)
        self._refresh_goblins()

    def _refresh_elves(self):
        pos, ranges = self._elves_pos, self._elf_ranges
        pos.clear()
        ranges.clear()
        for elf in self.elves:
            pos.add(elf.pos)
            ranges.update(neighbors(elf.pos))

    def _refresh_goblins(self):
        pos, ranges = self._goblins_pos, self._goblin_ranges
        pos.clear()
        ranges.clear()
        for goblin in self.goblins:
            pos.add(goblin.pos)
            ranges.update(neighbors(goblin.pos))

    @property
    def score(self):
        return self.rounds * sum(p.health for p in self.players if p.health > 0)

    def ordered_players(self):
        players = self.players
        ids = sorted(
            (i for i in range(len(players)) if players[i].health > 0),
            key=lambda i: players[i].pos,
        )
        return list(ids)

    @property
    def complete(self):
        return self._n_elves == 0 or self._n_goblins == 0

    def show_state(self, print_health=False):
        indices = ~self.playable * 1
        for elf in self.elves:
            indices[elf.pos] = 2
        for goblin in self.goblins:
            indices[goblin.pos] = 3
        full_map = np.choose(indices, ('.', '#', 'E', 'G'))

        lines = []
        for x, line in enumerate(full_map):
            line = "".join(line)
            if print_health:
                on_line = [p for p in self.players if p.x == x]
                on_line.sort(key=lambda p: p.y)
                line += "   " + ", ".join(
                    f"{p.clan[0].upper()}({p.health})"
                    for p in on_line
                    if p.health > 0
                )
            lines.append(line)

        return "\n".join(lines)

    def __str__(self):
        """Generate a fancy visualization of how the battle is doing"""
        return self.show_state()

    def next_move(self, player_id: int):
        player = self.players[player_id]
        if player.health <= 0:
            return player.pos

        ranges = self._goblin_ranges if player.clan == ELF else self._elf_ranges

        start_pos = player.pos
        if start_pos in ranges:
            return start_pos

        frontier, visited = [], self._goblins_pos | self._elves_pos
        for pos in neighbors(start_pos):
            if pos in visited or not self.playable[pos]:
                continue
            heappush(frontier, (1, pos, pos))
            visited.add(pos)

        while frontier:
            steps, first_pos, pos = heappop(frontier)
            if pos in ranges:
                return first_pos
            for next_pos in neighbors(pos):
                if next_pos in visited or not self.playable[next_pos]:
                    continue
                visited.add(next_pos)
                heappush(frontier, (steps + 1, first_pos, next_pos))

        return start_pos

    def play_turn(self, player_id: int, allow_elf_death=True):
        player = self.players[player_id]
        next_move = self.next_move(player_id)

        if next_move != player.pos:
            player.move(next_move)
            if player.clan == ELF:
                self._refresh_elves()
            else:
                self._refresh_goblins()

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
                self._kill_elf(target)
            else:
                self._kill_goblin(target)

        return True

    def play(self, allow_elf_death=True):
        while True:
            for player_id in self.ordered_players():
                if self.complete:
                    return True
                if self.players[player_id].health <= 0:
                    continue
                res = self.play_turn(player_id, allow_elf_death)
                if not allow_elf_death and not res:
                    return False
            self.rounds += 1


@lru_cache(maxsize=512)
def neighbors(pos: Tuple[int, int]):
    x, y = pos
    return [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]


def optimize_elf_attack(data: str):
    def try_value(atk_val: int):
        game = Game(data, elf_atk=atk_val)
        return game.play(allow_elf_death=False), game.score

    max_fail, min_pass = 2, 3
    while True:
        passed, opt_score = try_value(min_pass)
        if passed:
            break
        max_fail = min_pass
        min_pass *= 2

    while min_pass - max_fail > 1:
        pivot = (max_fail + min_pass) // 2
        passed, score = try_value(pivot)
        if passed:
            min_pass = pivot
            opt_score = score
        else:
            max_fail = pivot

    return min_pass, opt_score


def main(data: str):
    game = Game(data)
    game.play()
    yield game.score

    yield optimize_elf_attack(data)[1]
