from libaoc.constraints import Constraint, Solver, UniqueConstraint

#  A A A
# B     C
# B     C
#  D D D
# E     F
# E     F
#  G G G
VARS = "ABCDEFG"
DIGITS = [
    "ABC_EFG",  # 0
    "__C__F_",  # 1
    "A_CDE_G",  # 2
    "A_CDF_G",  # 3
    "_BCD_F_",  # 4
    "AB_D_FG",  # 5
    "AB_DEFG",  # 6
    "A_C__F_",  # 7
    "ABCDEFG",  # 8
    "ABCD_FG",  # 9
]
DIGIT_SETS = {
    frozenset(d.replace("_", "")): i
    for i, d in enumerate(DIGITS)
}
SIGNATURES: dict[str, list[int]] = {
    seg: [len(dig.replace("_", "")) for dig in DIGITS if seg in dig]
    for seg in VARS
}


class SegmentConstraint(Constraint[str, str]):
    def __init__(self, segment: str, observations: list[str]):
        super().__init__([segment])
        self.segment = segment
        self.observations = [set(s) for s in observations]

    def satisfied(self, assignment: dict[str, str]) -> bool:
        val = assignment[self.segment]
        matches = SIGNATURES[self.segment].copy()
        for obs in self.observations:
            if val not in obs:
                continue
            try:
                matches.remove(len(obs))
            except ValueError:
                return False
        return len(matches) == 0


def solve_segment_display(observations: list[str]) -> dict[str, str]:
    assert len(observations) == 10

    solver: Solver[str, str] = Solver(
        list(VARS), {seg: list(VARS.lower()) for seg in VARS}
    )
    solver.add_constraint(UniqueConstraint(list(VARS)))
    for seg in VARS:
        solver.add_constraint(SegmentConstraint(seg, observations))

    assignments = solver.solve()
    if assignments is None:
        raise ValueError("No solution!")
    return {v: k for k, v in assignments.items()}


def decode_number(observations: list[str], digits: list[str]) -> int:
    assignments = {ord(k): v for k, v in solve_segment_display(observations).items()}
    value = 0
    for digit in digits:
        value *= 10
        solved_digit = digit.translate(assignments)
        value += DIGIT_SETS[frozenset(solved_digit)]
    return value


def parse_data(data: str) -> list[tuple[list[str], list[str]]]:
    def parse_line(line: str):
        obs, _, digits = line.partition(" | ")
        return obs.split(), digits.split()
    return [parse_line(ln) for ln in data.strip().splitlines()]


def count_1478_digits(data: list[tuple[list[str], list[str]]]):
    return sum(
        sum(len(dig) in {2, 3, 4, 7} for dig in digits)
        for _, digits in data
    )


def decode_data(data: list[tuple[list[str], list[str]]]) -> int:
    return sum(decode_number(obs, dig) for obs, dig in data)


def main(data: str):
    data = parse_data(data)
    yield count_1478_digits(data)
    yield decode_data(data)
