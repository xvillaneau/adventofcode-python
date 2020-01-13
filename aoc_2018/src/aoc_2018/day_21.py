from .day_19 import Program, OPERATIONS


def shortest_run(pointer_addr: int, program: Program):
    pointer, max_p = 0, len(program)
    registers = [0] * 6

    while 0 <= pointer < max_p:
        registers[pointer_addr] = pointer
        op, a, b, c = program[pointer]
        if b == 0 and op is OPERATIONS["eqrr"]:
            registers[0] = registers[a]
        op(a, b, c, registers)
        pointer = registers[pointer_addr] + 1

    return registers


def cheat_program():
    """Result of reverse-engineering my puzzle input"""
    b = 0
    while True:
        d = b | 65536
        b = 16298264

        while True:
            b += d & 255
            b &= 16777215
            b *= 65899
            b &= 16777215
            if d < 256:
                break
            d //= 256

        yield b


def main(_: str):

    program = cheat_program()
    first_res = next(program)
    yield first_res

    visited, last_res = {first_res}, first_res
    while (res := next(program)) not in visited:
        visited.add(res)
        last_res = res
    yield last_res
