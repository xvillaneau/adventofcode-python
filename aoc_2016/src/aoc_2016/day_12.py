from typing import Callable, List, Optional

Operation = Callable[[List[int]], Optional[int]]
Program = List[Operation]

ADDRESSES = {"a": 0, "b": 1, "c": 2, "d": 3}


def parse_cpy(x, y) -> Operation:
    y = ADDRESSES[y]

    try:
        x = int(x)

    except ValueError:
        x = ADDRESSES[x]

        def cpy(registers: List[int]):
            registers[y] = registers[x]

    else:

        def cpy(registers: List[int]):
            registers[y] = x

    return cpy


def parse_jnz(x, y) -> Operation:
    y = int(y)

    try:
        x = int(x)

    except ValueError:
        x = ADDRESSES[x]

        def jnz(registers: List[int]):
            if registers[x] != 0:
                return y
            return 1

    else:
        jump = y if x else 1

        def jnz(_):
            return jump

    return jnz


def parse_inc(x):
    x = ADDRESSES[x]

    def inc(registers: List[int]):
        registers[x] += 1

    return inc


def parse_dec(x):
    x = ADDRESSES[x]

    def dec(registers: List[int]):
        registers[x] -= 1

    return dec


PARSERS = {
    "cpy": parse_cpy,
    "inc": parse_inc,
    "dec": parse_dec,
    "jnz": parse_jnz,
}


def parse_code(data: str):
    program = []
    for line in data.splitlines():
        op, *args = line.split()
        program.append(PARSERS[op](*args))
    return program


def run_code(program: Program, ini: List[int] = ()):
    if ini:
        registers = list(ini)
    else:
        registers = [0] * 4
    pointer = 0
    while 0 <= pointer < len(program):
        res = program[pointer](registers)
        pointer += 1 if not res else res
    return registers


def main(data: str):
    program = parse_code(data)
    yield run_code(program)[0]
    yield run_code(program, [0, 0, 1, 0])[0]
