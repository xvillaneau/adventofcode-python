from typing import Callable, List, Optional

Operation = Callable[[List[int]], Optional[int]]
Program = List[Operation]

ADDRESSES = {"a": 0, "b": 1, "c": 2, "d": 3}


def value_getter(arg):
    try:
        arg = int(arg)

    except ValueError:
        arg = ADDRESSES[arg]
        def getter(registers):
            return registers[arg]

    else:
        def getter(_):
            return arg

    return getter


def parse_cpy(x, y) -> Operation:
    y = ADDRESSES[y]
    get_x = value_getter(x)

    def cpy(registers: List[int]):
        registers[y] = get_x(registers)

    return cpy


def parse_jnz(x, y) -> Operation:
    get_x = value_getter(x)
    get_y = value_getter(y)

    def jnz(registers):
        if get_x(registers) != 0:
            return get_y(registers)
        return 1

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
