from .intcode import ASCIIRunner, parse_intcode

PART_1 = ["NOT A J", "NOT B T", "OR T J", "NOT C T", "OR T J", "AND D J", "WALK"]
PART_2 = PART_1[:-1] + ["NOT E T", "NOT T T", "OR H T", "AND T J", "RUN"]


def main(data: str):
    code = parse_intcode(data)
    yield ASCIIRunner(code).program_run(PART_1)
    yield ASCIIRunner(code).program_run(PART_2)
