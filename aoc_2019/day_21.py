from aoc_2019.intcode import ASCIIRunner, read_program

PART_1 = ["NOT A J", "NOT B T", "OR T J", "NOT C T", "OR T J", "AND D J", "WALK"]
PART_2 = PART_1[:-1] + ["NOT E T", "NOT T T", "OR H T", "AND T J", "RUN"]


def part_1(code):
    return ASCIIRunner(code).program_run(PART_1)


def part_2(code):
    return ASCIIRunner(code).program_run(PART_2)


if __name__ == '__main__':
    from libaoc import simple_main
    simple_main(2019, 21, read_program, part_1, part_2)
