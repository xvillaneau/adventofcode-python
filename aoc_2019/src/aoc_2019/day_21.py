from libaoc import BaseRunner
from .intcode import ASCIIRunner

PART_1 = ["NOT A J", "NOT B T", "OR T J", "NOT C T", "OR T J", "AND D J", "WALK"]
PART_2 = PART_1[:-1] + ["NOT E T", "NOT T T", "OR H T", "AND T J", "RUN"]


def part_1(code):
    return ASCIIRunner(code).program_run(PART_1)


def part_2(code):
    return ASCIIRunner(code).program_run(PART_2)


class AocRunner(BaseRunner):
    year = 2019
    day = 21
    parser = BaseRunner.int_list_parser(",")

    def run(self, code):
        yield part_1(code)
        yield part_2(code)
