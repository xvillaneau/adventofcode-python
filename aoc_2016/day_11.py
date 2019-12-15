
from dataclasses import dataclass
from itertools import combinations
from typing import FrozenSet, Set, Tuple

TEST = """
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
"""


@dataclass(frozen=True)
class Equipment:
    name: str
    gen_floor: int
    chip_floor: int

    def move(self, gen_move, chip_move) -> 'Equipment':
        return Equipment(self.name, self.gen_floor + gen_move, self.chip_floor + chip_move)


@dataclass(frozen=True)
class LabState:
    elevator: int
    equipment: FrozenSet[Equipment]

    def move(self, gen_move, chip_move, names) -> 'LabState':
        """VERY DUMB FUNCTION! Hopefully your input is right"""
        return LabState(self.elevator + (gen_move or chip_move), frozenset(
            (eqp.move(gen_move, chip_move) if eqp.name in names else eqp)
            for eqp in self.equipment))

    def final(self) -> 'LabState':
        return LabState(4, frozenset(Equipment(eqp.name, 4, 4) for eqp in self.equipment))

    def is_valid(self) -> bool:
        unsafe, lone_chips = set([]), set([])
        for eqp in self.equipment:
            if eqp.chip_floor != eqp.gen_floor:
                lone_chips.add(eqp.chip_floor)
            unsafe.add(eqp.gen_floor)
            if unsafe & lone_chips:
                return False
        return True

    def is_final(self) -> bool:
        return all(eqp.chip_floor == eqp.gen_floor == 4 for eqp in self.equipment)

    def next_states(self) -> Set['LabState']:
        floor = self.elevator
        next_states = set(())

        chips_here = frozenset(e.name for e in self.equipment if e.chip_floor == floor)
        gens_here = frozenset(e.name for e in self.equipment if e.gen_floor == floor)

        for move in (1, -1):
            if not 1 <= floor + move <= 4:
                continue
            for name in chips_here & gens_here:  # Move both G and M at once
                next_states.add(self.move(move, move, (name,)))
            for name in gens_here:  # Move single G
                next_states.add(self.move(move, 0, (name,)))
            for name in chips_here:  # Move single M
                next_states.add(self.move(0, move, (name,)))
            for na, nb in combinations(gens_here, 2):  # Move two Gs
                next_states.add(self.move(move, 0, (na, nb)))
            for na, nb in combinations(chips_here, 2):  # Move two Ms
                next_states.add(self.move(0, move, (na, nb)))

        return {s for s in next_states if s.is_valid()}

    def __str__(self):
        equipment = sorted(self.equipment, key=lambda eqp: eqp.name)
        header = "      " + " ".join(eqp.name[:3] + "." for eqp in equipment)

        def _repr_eqp(eqp: Equipment, floor: int):
            gen_str = "G" if eqp.gen_floor == floor else "."
            chip_str = "M" if eqp.chip_floor == floor else "."
            return f'{gen_str} {chip_str}'

        floors = [f'F{n} {"E" if self.elevator == n else "."}  ' +
                  '  '.join(_repr_eqp(e, n) for e in equipment)
                  for n in range(4, 0, -1)]

        return '\n'.join([header] + floors)


@dataclass(frozen=True)
class IntState:
    floor: int
    n_eqp: int
    eqp: int

    def mk_final(self):
        return IntState(3, self.n_eqp, (1 << (8 * self.n_eqp)) - 1)

    def is_final(self):
        return self.eqp + 1 == 1 << (8 * self.n_eqp)

    @classmethod
    def from_tuples(cls, floor: int, *eqp_tuples: Tuple[int, int]):
        nums = [i for t in eqp_tuples for i in t]
        assert all(0 <= i < 4 for i in nums)
        assert 0 <= floor < 4
        eqp_num = sum(1 << (n+4*i) for i, n in enumerate(nums))
        return IntState(floor, len(eqp_tuples), eqp_num)


TEST_START = LabState(1, frozenset([Equipment('hydrogen', 2, 1), Equipment('lithium', 3, 1),
                                    Equipment('calcium', 3, 3)]))

DAY11_START = LabState(1, frozenset([
    Equipment('promethium', 1, 1), Equipment('cobalt', 2, 3), Equipment('curium', 2, 3),
    Equipment('ruthenium', 2, 3), Equipment('plutonium', 2, 3)]))

DAY11_2_START = LabState(1, frozenset([
    Equipment('promethium', 1, 1), Equipment('cobalt', 2, 3), Equipment('curium', 2, 3),
    Equipment('ruthenium', 2, 3), Equipment('plutonium', 2, 3),
    Equipment('elerium', 1, 1), Equipment('dilithium', 1, 1)]))

if __name__ == '__main__':
    # from libaoc.algo import least_steps
    from libaoc.algo import least_steps_both_ends

    # print(least_steps(TEST_START, LabState.next_states, LabState.is_final))
    print(least_steps_both_ends(DAY11_2_START, DAY11_2_START.final(), LabState.next_states))
