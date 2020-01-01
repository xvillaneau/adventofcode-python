from itertools import chain, compress
import re
import numpy as np

from libaoc.primes import extended_euclidian_algorithm


def deal_new_stack(deck):
    return deck[::-1]


def cut_stack(deck, n):
    return np.roll(deck, -n)


def deal_with_increment(deck, n):
    r = len(deck)
    ind = np.arange(r)
    rev_ind = (ind * n) % r
    np.put(ind, rev_ind, np.arange(r))
    return deck[ind]


def parse_techniques(techniques):
    commands = []
    for line in techniques:
        if line == "deal into new stack":
            commands.append((0, 0))
        elif m := re.match(r"cut (-?\d+)", line):
            commands.append((1, int(m.group(1))))
        elif m := re.match(r"deal with increment (\d+)", line):
            commands.append((2, int(m.group(1))))
        else:
            raise ValueError(f"Bad line: {line}")
    return commands


def follow_card(commands, card: int, deck_size):
    position = card
    for cmd, arg in commands:
        if cmd == 0:
            position = deck_size - position - 1
        elif cmd == 1:
            position = (position - arg) % deck_size
        else:  # incr
            position = (position * arg) % deck_size
    return position


def revert_card(commands, position: int, deck_size):
    for cmd, arg in commands[::-1]:
        if cmd == 0:
            position = deck_size - position - 1
        elif cmd == 1:
            position = (position + arg) % deck_size
        else:  # incr
            p, _, _ = extended_euclidian_algorithm(arg, deck_size)
            position = (p * position) % deck_size
    return position


def merge_commands(commands, deck_size):
    zero = follow_card(commands, 0, deck_size)
    one = follow_card(commands, 1, deck_size)
    offset = deck_size - zero
    increment = (one - zero) % deck_size
    return [(2, increment), (1, offset)]


def merge_commands_n_times(commands, deck_size, n_steps: int):
    components = [merge_commands(commands, deck_size)]
    while len(components) < n_steps.bit_length():
        components.append(merge_commands(components[-1] + components[-1], deck_size))
    bits = [b == "1" for b in bin(n_steps)[:1:-1]]
    sub_cmds = list(chain.from_iterable(compress(components, bits)))
    return merge_commands(sub_cmds, deck_size)


def main(data: str):
    commands = parse_techniques(data.splitlines())
    yield follow_card(commands, 2019, 10007)

    deck_size, n_steps = 119_315_717_514_047, 101_741_582_076_661
    merged_commands = merge_commands_n_times(commands, deck_size, n_steps)
    yield revert_card(merged_commands, 2020, deck_size)
