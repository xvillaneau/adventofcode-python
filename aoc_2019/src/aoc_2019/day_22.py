from itertools import chain, compress
from typing import List, Tuple

from libaoc.primes import extended_euclidian_algorithm


DEAL_NEW, CUT, DEAL_INCREMENT = 0, 1, 2
Techniques = List[Tuple[int, int]]


def parse_techniques(data: str) -> Techniques:
    """
    Read the human-friendly instructions and convert them into machine
    instructions. Instructions are tuple of (operation, argument) where
    0 is "deal new", 1 is "cut", 2 is "deal with increment".
    """

    def parse_line(line: str):
        if line == "deal into new stack":
            return DEAL_NEW, 0
        elif line.startswith("cut"):
            return CUT, int(line.rpartition(" ")[2])
        elif line.startswith("deal with increment"):
            return DEAL_INCREMENT, int(line.rpartition(" ")[2])
        else:
            raise ValueError(f"Bad line: {line}")

    return [parse_line(_line) for _line in data.splitlines()]


def follow_card(techniques: Techniques, deck_size: int, position: int) -> int:
    """Compute the position of a card after shuffling"""
    for cmd, arg in techniques:
        if cmd == DEAL_NEW:
            position = deck_size - position - 1
        elif cmd == CUT:
            position = (position - arg) % deck_size
        else:  # DEAL_INCREMENT
            position = (position * arg) % deck_size
    return position


def revert_card(techniques: Techniques, deck_size: int, position: int) -> int:
    """Compute the starting position corresponding to a final position"""
    for cmd, arg in techniques[::-1]:
        if cmd == DEAL_NEW:
            # Reverse of "deal new" is itself
            position = deck_size - position - 1
        elif cmd == CUT:
            # Reverse of "cut" is the same with negative argument
            position = (position + arg) % deck_size
        else:  # DEAL_INCREMENT
            # Reversing "deal with increment" requires some maths
            p, _, _ = extended_euclidian_algorithm(arg, deck_size)
            position = (position * p) % deck_size
    return position


def merge_techniques(techniques: Techniques, deck_size: int) -> Techniques:
    """
    Here is the core magic for part 2: it turns out that ANY set of
    techniques is ALWAYS equivalent to one "deal with increment"
    followed by a cut. Any we only need to know the end positions of
    cards 0 and 1 to figure out the equivalence.
    """
    pos_zero = follow_card(techniques, deck_size, 0)
    pos_one = follow_card(techniques, deck_size, 1)
    offset = deck_size - pos_zero
    increment = (pos_one - pos_zero) % deck_size
    return [(DEAL_INCREMENT, increment), (CUT, offset)]


def merge_commands_n_times(
    techniques: Techniques, deck_size: int, n_steps: int
) -> Techniques:
    """
    Compute the equivalent deal + cut (see above) to a given list of
    techniques applied many times in a row.
    """
    # The components list holds in each cell the equivalent deal + cut
    # applying the techniques 2 ** i times (where i is the position in
    # the list). We initialize it with 2 ** 0 = 1 applications.
    components = [merge_techniques(techniques, deck_size)]

    # Build the components by doubling the techniques until we have
    # as many as our input step count is large in base 2.
    while len(components) < n_steps.bit_length():
        components.append(merge_techniques(components[-1] * 2, deck_size))

    # Build an equivalent set of techniques to the number of repeats
    # by decomposing that number in binary and picking the components
    bits = [b == "1" for b in bin(n_steps)[:1:-1]]
    sub_cmds = list(chain.from_iterable(compress(components, bits)))

    # Merge the binary decomposition to get the result!
    return merge_techniques(sub_cmds, deck_size)


def main(data: str):
    """Main routine for AoC 2019 day 22"""
    techniques = parse_techniques(data)
    yield follow_card(techniques, 10007, 2019)

    deck_size, n_steps = 119_315_717_514_047, 101_741_582_076_661
    merged_techniques = merge_commands_n_times(techniques, deck_size, n_steps)
    yield revert_card(merged_techniques, deck_size, 2020)
