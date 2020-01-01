from dataclasses import dataclass
from enum import Enum
from operator import attrgetter
from types import SimpleNamespace
from typing import NamedTuple

from libaoc.algo import CostAStarSearch

# Constants

SETTINGS = SimpleNamespace()
SETTINGS.DEBUG = False
MAGIC_MISSILE_DMG = 4
DRAIN_POINTS = 2
SHIELD_ARMOR = 7
SHIELD_TURNS = 6
POISON_DMG = 3
POISON_TURNS = 6
RECHARGE_MANA = 101
RECHARGE_TURNS = 5

class Action(Enum):
    MagicMissile = ("Magic Missile", 53)
    Drain = ("Drain", 73)
    Shield = ("Shield", 113)
    Poison = ("Poison", 173)
    Recharge = ("Recharge", 229)

    def __new__(cls, name, cost=0):
        obj = object.__new__(cls)
        obj._value_ = name
        obj.cost = cost
        return obj


# Immutable state objects

class _Player(NamedTuple):
    hit_points: int
    mana: int
    armor: int

class _Boss(NamedTuple):
    hit_points: int
    damage: int

class _Effects(NamedTuple):
    shields: int
    poison: int
    recharge: int

class _State(NamedTuple):
    player: _Player
    boss: _Boss
    effects: _Effects
    hard: bool

    @property
    def won(self):
        return self.boss.hit_points <= 0

    @property
    def lost(self):
        return self.player.hit_points <= 0

    def __repr__(self):
        effects = [f'{k}:{v}' for k, v in self.effects._asdict().items() if v]
        return (
            f"<State player HP={self.player.hit_points} mana={self.player.mana}, "
            f"boss HP={self.boss.hit_points}, "
            f"effects={' '.join(effects) or 'none'}>"
        )

    def available_actions(self):
        actions = {Action.MagicMissile, Action.Drain}
        if self.effects.shields <= 1:
            actions.add(Action.Shield)
        if self.effects.poison <= 1:
            actions.add(Action.Poison)
        if self.effects.recharge <= 1:
            actions.add(Action.Recharge)
        mana = self.player.mana
        return {act for act in actions if act.cost <= mana}

    def successors(self):
        result = []
        for action in self.available_actions():
            fight = Fight.from_state(self)
            fight.play_round(action)
            if not fight.lost:
                result.append((fight.to_state(), action.cost))
        return result


def make_initial(player_hp, player_mana, boss_hp, boss_damage, hard=False):
    player = _Player(player_hp, player_mana, 0)
    boss = _Boss(boss_hp, boss_damage)
    effects = _Effects(0, 0, 0)
    return _State(player, boss, effects, hard)


# Mutable objects with logic

@dataclass
class Player:
    hit_points: int
    mana: int
    armor: int

    def __str__(self):
        hp = self.hit_points
        return (
            f"Player has {hp} hit point{'s' if hp == 1 else ''}, "
            f"{self.armor} armor, {self.mana} mana"
        )

    def __iter__(self):
        return iter((self.hit_points, self.mana, self.armor))

    def hit(self, damage: int):
        self.hit_points -= max(1, damage - self.armor)

    def heal(self, point: int):
        self.hit_points += point

    def spend(self, mana: int):
        self.mana -= mana

    def recharge(self, mana: int):
        self.mana += mana


@dataclass
class Boss:
    hit_points: int
    damage: int

    def __str__(self):
        hp = self.hit_points
        return f"Boss has {hp} hit point{'s' if hp == 1 else ''}"

    def __iter__(self):
        return iter((self.hit_points, self.damage))

    def hit(self, damage: int):
        self.hit_points -= damage


@dataclass
class Effects:
    shields: int
    poison: int
    recharge: int

    def __iter__(self):
        return iter((self.shields, self.poison, self.recharge))


@dataclass
class Fight:
    player: Player
    boss: Boss
    effects: Effects
    hard: bool = False
    debug: bool = False

    @property
    def won(self):
        return self.boss.hit_points <= 0

    @property
    def lost(self):
        return self.player.hit_points <= 0

    def log(self, msg, condition=True):
        if not (self.debug and condition):
            return
        print(msg)

    @classmethod
    def from_state(cls, state: _State):
        player = Player(*state.player)
        boss = Boss(*state.boss)
        effects = Effects(*state.effects)
        return cls(player, boss, effects,  hard=state.hard, debug=SETTINGS.DEBUG)

    def to_state(self):
        player = _Player(*self.player)
        boss = _Boss(*self.boss)
        effects = _Effects(*self.effects)
        return _State(player, boss, effects, self.hard)

    def apply_effects(self):

        if self.effects.shields > 1:
            self.effects.shields -= 1
            self.log(f"Shield's timer is now {self.effects.shields}")
            self.player.armor = SHIELD_ARMOR
        elif self.effects.shields == 1:
            self.log(f"Shield wears off, decreasing armor by {SHIELD_ARMOR}.")
            self.effects.shields = 0
            self.player.armor = 0
        else:
            self.player.armor = 0

        if self.effects.poison:
            self.effects.poison -= 1
            self.log(f"Poison deals {POISON_DMG} damage; its timer is now {self.effects.poison}")
            self.boss.hit(POISON_DMG)
            self.log("Poison wears off", not self.effects.poison)

        if self.effects.recharge:
            self.effects.recharge -= 1
            self.log(f"Recharge provides {RECHARGE_MANA} mana; its timer is now {self.effects.recharge}")
            self.player.recharge(RECHARGE_MANA)
            self.log("Recharge wears off", not self.effects.recharge)

    def player_action(self, action: Action):
        if self.won or self.lost:
            raise RuntimeError("Fight already over")

        cost = action.cost
        if self.player.mana < cost:
            raise RuntimeError("Cannot cast a spell without mana!")

        act_str = f"Player casts {action.value}"

        if action == Action.MagicMissile:
            self.log(f"{act_str}, dealing {MAGIC_MISSILE_DMG} damage.")
            self.boss.hit(MAGIC_MISSILE_DMG)

        elif action == Action.Drain:
            self.log(f"{act_str}, dealing {DRAIN_POINTS} damage, and healing {DRAIN_POINTS} HP.")
            self.boss.hit(DRAIN_POINTS)
            self.player.heal(DRAIN_POINTS)

        elif action == Action.Shield:
            self.log(f"{act_str}, increasing armor by {SHIELD_ARMOR}.")
            if self.effects.shields > 0:
                raise RuntimeError("Shields are still in use!")
            self.effects.shields = SHIELD_TURNS
            self.player.armor = SHIELD_ARMOR

        elif action == Action.Poison:
            self.log(f"{act_str}.")
            if self.effects.poison > 0:
                raise RuntimeError("Poison is still in use!")
            self.effects.poison = POISON_TURNS

        elif action == Action.Recharge:
            self.log(f"{act_str}.")
            if self.effects.recharge > 0:
                raise RuntimeError("Recharge is still in use!")
            self.effects.recharge = RECHARGE_TURNS

        self.player.spend(cost)

    def boss_action(self):
        dmg, armor = self.boss.damage, self.player.armor
        dmg_str = (
            f"{dmg} - {armor} = {max(1, dmg - armor)}"
            if armor
            else str(dmg)
        )
        self.log(f"Boss attacks for {dmg_str} damage!")
        self.player.hit(dmg)

    def play_round(self, action: Action):
        self.log("\n=== Start round! ===")
        self.log(f"== Player turn ==\n- {self.player}\n- {self.boss}")

        if self.hard:
            self.log("HARD MODE: Player loses 1 health!")
            self.player.hit(1)
            if self.lost:
                self.log("This kills the player, and the boss wins :(")
                return

        self.apply_effects()
        if self.won:
            self.log("This kills the boss, and the player wins!")
            return

        self.player_action(action)
        if self.won:
            self.log("This kills the boss, and the player wins!")
            return

        self.log(f"\n== Boss turn ==\n- {self.player}\n- {self.boss}")
        self.apply_effects()
        if self.won:
            self.log("This kills the boss, and the player wins!")
            return

        self.boss_action()
        self.log("This kills the player, and the boss wins :(", self.lost)


def least_mana(game_data, hard=False):
    initial = make_initial(*game_data, hard=hard)
    a_star = CostAStarSearch(initial, attrgetter("won"), _State.successors)
    result = a_star.search()
    return int(result.cost)

if __name__ == '__main__':
    from functools import partial
    from libaoc import simple_main, static_input
    part_1, part_2 = least_mana, partial(least_mana, hard=True)
    simple_main(2015, 22, static_input((50, 500, 51, 9)), part_1, part_2)
