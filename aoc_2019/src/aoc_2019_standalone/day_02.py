import sys


def run_computer(code, noun, verb):
    # The memory will be written to, and we don't want the input to be
    # affected by that. It would create some interesting bugs.
    memory = code.copy()
    # Initialize the parameters in memory
    memory[1], memory[2] = noun, verb

    p = 0
    while True:
        op = memory[p]
        if op == 99:  # Halt the program
            return memory[0]
        # Read the arguments
        a, b, c = memory[p + 1], memory[p + 2], memory[p + 3]
        if op == 1:  # Addition
            memory[c] = memory[a] + memory[b]
        elif op == 2:  # Multiplication
            memory[c] = memory[a] * memory[b]
        else:
            raise RuntimeError(f"Unknown operation {op}")
        # Move to the next instruction
        p += 4


def locate_target(code, target):
    """Find which input returns the given target. The hard way."""
    noun, verb = next(
        (noun, verb)
        for noun in range(100)
        for verb in range(100)
        if run_computer(code, noun, verb) == target
    )
    return noun * 100 + verb


def parse_program(filename):
    with open(filename, "r") as file:
        return [int(num) for num in file.read().split(",")]


def main(filename):
    code = parse_program(filename)
    part_1 = run_computer(code, noun=12, verb=2)
    print("Day 2, part 1:", part_1)
    part_2 = locate_target(code, 19690720)
    print("Day 2, part 2:", part_2)


if __name__ == "__main__":
    main(sys.argv[1])
