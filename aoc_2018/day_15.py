from dataclasses import dataclass
from typing import Tuple, List
import numpy as np

TEST_1 = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
"""

TEST_2 = """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
"""

TEST_3 = """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
"""

TEST_4 = """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
"""

Pos = Tuple[int, int]


@dataclass
class Soldier:
    x: int
    y: int
    clan: str
    attack: int = 3
    health: int = 200

    @property
    def pos(self):
        return self.x, self.y


class CannotMove(Exception):
    pass


class EndOfBattle(Exception):
    pass


def parse_map(map_str: str):
    """From an input text map, generate the playable areas and the players"""
    chars_mat = np.array([list(l) for l in map_str.strip().splitlines()])
    playable = chars_mat != '#'
    elves = [Soldier(x, y, 'elf') for x, y in zip(*np.nonzero(chars_mat == 'E'))]
    goblins = [Soldier(x, y, 'goblin') for x, y in zip(*np.nonzero(chars_mat == 'G'))]
    return playable, elves, goblins


def print_battle(playable, elves, goblins):
    """Generate a fancy visualization of how the battle is doing"""
    chars = ('.', '#', 'E', 'G')
    m_elves = mat_from_soldiers(playable, elves)
    m_goblins = mat_from_soldiers(playable, goblins)
    return '\n'.join(''.join(map(chars.__getitem__, l))
                     for l in ~playable * 1 + m_elves * 2 + m_goblins * 3)


def mat_from_soldiers(playable, soldiers: List[Soldier]):
    out = np.full(playable.shape, False)
    for soldier in soldiers:
        out[soldier.x, soldier.y] = True
    return out


# TODO: Fix me

def reach_steps(free, pos: Pos, *, limit=None):

    if limit is None:
        lx, ly = free.shape
        limit = lx * ly

    steps = np.full(free.shape, -1)
    border = np.full(free.shape, False)
    n_steps = 0
    x, y = pos
    border[x, y] = True
    while border.any() and n_steps <= limit:
        ix, iy = np.where(border)
        steps[ix, iy] = n_steps
        n_steps += 1
        border = ndimage.binary_dilation(border) & (steps == -1) & free
    return steps


def all_target_range(playable, allies, enemies):
    free = playable & ~allies & ~enemies
    return ndimage.binary_dilation(enemies) & free


def adjacent_pos(pos: Pos):
    x, y = pos
    return [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]


def next_move_to_target(playable, allies, enemies, pos: Pos):
    free = playable & ~allies & ~enemies
    enemy_ranges = all_target_range(playable, allies, enemies)
    steps_away = reach_steps(free, pos)
    reachable_ranges = enemy_ranges & (steps_away > -1)
    if not reachable_ranges.any():
        raise CannotMove()
    idx, idy = np.nonzero(reachable_ranges)
    target_tuples = np.concatenate((steps_away[idx, idy], idx, idy)).reshape(3, len(idx)).transpose()
    dist, tx, ty = min(tuple(l) for l in target_tuples)
    for nx, ny in adjacent_pos(pos):
        if not free[nx, ny]:
            continue
        steps_from_next = reach_steps(free, (nx, ny), limit=dist-1)
        if steps_from_next[tx, ty] == dist - 1:
            return nx, ny


def move(playable, allies: List[Soldier], enemies: List[Soldier], soldier: Soldier):
    cur_adjacent = adjacent_pos(soldier.pos)
    if any(s.pos in cur_adjacent for s in enemies):
        return  # Already in range: don't move!

    mat_allies = mat_from_soldiers(playable, allies)
    mat_enemies = mat_from_soldiers(playable, enemies)

    nx, ny = next_move_to_target(playable, mat_allies, mat_enemies, soldier.pos)
    soldier.x = nx
    soldier.y = ny


def turn(playable, elves: List[Soldier], goblins: List[Soldier], soldier: Soldier):

    is_elf = soldier in elves
    allies, enemies = (elves, goblins) if is_elf else (goblins, elves)
    if not enemies:
        raise EndOfBattle
    try:
        move(playable, allies, enemies, soldier)
    except CannotMove:
        return  # End of turn

    cur_adjacent = adjacent_pos(soldier.pos)
    targets = [s for s in enemies if s.pos in cur_adjacent]
    if not targets:
        return

    target = min(targets, key=lambda s: (s.health, s.x, s.y))
    target.health -= soldier.attack
    if target.health <= 0:  # Target down
        enemies.remove(target)


def play_round(playable, elves: List[Soldier], goblins: List[Soldier]):
    order = list(sorted(elves + goblins, key=lambda s: s.pos))
    for soldier in order:
        if soldier.health <= 0:
            continue
        turn(playable, elves, goblins, soldier)


def game(full_input: str):
    playable, elves, goblins = parse_map(full_input)
    rounds = 0
    while True:
        try:
            play_round(playable, elves, goblins)
        except EndOfBattle:
            break
        rounds += 1
    return rounds, (elves if elves else goblins)


def main(full_input: str):
    rounds, winners = game(full_input)
    score = sum(s.health for s in winners)
    return rounds * score, ''
