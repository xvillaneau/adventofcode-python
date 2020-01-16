from functools import wraps
from math import factorial
from typing import List

from .day_12 import parse_cpy, parse_dec, parse_inc, parse_jnz, value_getter


def noop(_):
    pass


def make_toggled_parser(op_factory, toggle_factory, *args):
    try:
        func = op_factory(*args)
    except (ValueError, LookupError):
        func = noop

    @wraps(func)
    def wrapper(registers, *_):
        return func(registers)

    wrapper.toggle = lambda: toggle_factory(*args)
    return wrapper


def toggled_cpy(x, y):
    return make_toggled_parser(parse_cpy, toggled_jnz, x, y)


def toggled_jnz(x, y):
    return make_toggled_parser(parse_jnz, toggled_cpy, x, y)


def toggled_inc(x):
    return make_toggled_parser(parse_inc, toggled_dec, x)


def toggled_dec(x):
    return make_toggled_parser(parse_dec, toggled_inc, x)


def parse_tgl(x):
    get_x = value_getter(x)

    def tgl(registers, program, pointer):
        ind = pointer + get_x(registers)
        if 0 <= ind < len(program):
            op = program[ind]
            program[ind] = op.toggle()

    tgl.toggle = lambda: toggled_inc(x)
    return tgl


OPERATIONS = {
    "cpy": toggled_cpy,
    "jnz": toggled_jnz,
    "inc": toggled_inc,
    "dec": toggled_dec,
    "tgl": parse_tgl,
}


def parse_program(data: str):
    program = []
    for line in data.splitlines():
        line = line.split("#", maxsplit=1)[0]
        op, *args = line.split()
        program.append(OPERATIONS[op](*args))
    return program


def run_program(program, initial: List[int] = ()):
    if initial:
        registers = list(initial)
    else:
        registers = [0] * 4
    pointer = 0
    while 0 <= pointer < len(program):
        op = program[pointer]
        res = op(registers, program, pointer)
        pointer += 1 if not res else res
    return registers


def cheat_code(digit: int):
    return factorial(digit) + 80 * 94


def main(data: str):
    program = parse_program(data)
    registers = run_program(program, [7, 0, 0, 0])
    yield registers[0]
    assert registers[0] == cheat_code(7)
    yield cheat_code(12)
