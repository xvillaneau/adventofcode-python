"""
Advent of Code 2019 day 2, "Conventional" solution
https://adventofcode.com/2019/day/2

For a longer explanation of the problem and my solution, read:
https://github.com/xvillaneau/adventofcode-python/wiki/AoC-2019-Day-2
"""
import sys


def run_computer(code):
    # The memory will be written to, and we don't want the input to be
    # affected by that. It would create some interesting bugs.
    memory = code.copy()
    pointer = 0
    while True:
        opcode = memory[pointer]
        if opcode == 99:  # Halt the program
            return memory
        # Read the arguments
        arg_1, arg_2, arg_3 = memory[pointer + 1 : pointer + 4]
        if opcode == 1:  # Addition
            memory[arg_3] = memory[arg_1] + memory[arg_2]
        elif opcode == 2:  # Multiplication
            memory[arg_3] = memory[arg_1] * memory[arg_2]
        else:
            raise RuntimeError(f"Got unknown opcode {opcode}")
        pointer += 4  # Move to the next instruction


def gravity_assist(code, noun, verb):
    code[1], code[2] = noun, verb
    return run_computer(code)[0]


def find_input_values(code, target):
    """Find which input returns the given target. The hard way."""
    return next(
        noun * 100 + verb
        for noun in range(100)
        for verb in range(100)
        if gravity_assist(code, noun, verb) == target
    )


def parse_program(filename):
    with open(filename, "r") as file:
        return [int(num) for num in file.read().split(",")]


def main(filename):
    code = parse_program(filename)
    part_1 = gravity_assist(code, noun=12, verb=2)
    print("Day 2, part 1:", part_1)
    part_2 = find_input_values(code, 19690720)
    print("Day 2, part 2:", part_2)


if __name__ == "__main__":
    main(sys.argv[1])
