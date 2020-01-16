from collections import defaultdict
from functools import partial
from typing import Callable, Dict, List, Tuple, Union

Address = str
Value = int
Pointer = int
AddOrVal = Union[Address, Value]
Registers = Dict[Address, Value]
Operation = Callable[[Registers], Pointer]
Program = List[Tuple[str, Operation]]


def _reg_or_val(val: AddOrVal, regs: Registers) -> Value:
    return regs[val] if isinstance(val, str) else val


def op_set(address: Address, val: AddOrVal, regs: Registers) -> Pointer:
    regs[address] = _reg_or_val(val, regs)
    return 1


def op_sub(address: Address, val: AddOrVal, regs: Registers) -> Pointer:
    regs[address] -= _reg_or_val(val, regs)
    return 1


def op_mul(address: Address, val: AddOrVal, regs: Registers) -> Pointer:
    regs[address] *= _reg_or_val(val, regs)
    return 1


def op_jnz(test: AddOrVal, jump: AddOrVal, regs: Registers) -> Pointer:
    if _reg_or_val(test, regs) == 0:
        return 1
    j = _reg_or_val(jump, regs)
    if j == 0:
        raise ValueError("Infinite loop detected!")
    return j


def read_program(lines: List[str]) -> Program:

    funcs = {'set': op_set, 'sub': op_sub, 'mul': op_mul, 'jnz': op_jnz}

    def _str_or_int(thing: str) -> AddOrVal:
        try:
            return int(thing)
        except ValueError:
            return thing

    def _read_line(line: str) -> Tuple[str, Operation]:
        elems = line.split()
        assert len(elems) == 3
        name, arg_1, arg_2 = elems
        op = partial(funcs[name], _str_or_int(arg_1), _str_or_int(arg_2))
        return name, op

    return [_read_line(l) for l in lines if l.strip()]


def run_program(program: Program, debug=True) -> int:

    registers = defaultdict(int)
    registers['a'] = int(not debug)
    pointer, count_mul = 0, 0

    while 0 <= pointer < len(program):
        name, op = program[pointer]
        pointer += op(registers)
        if name == 'mul':
            count_mul += 1

    return count_mul


def f_test(b):

    def _test(d):
        e, r = divmod(b, d)
        return r == 0 and e >= 2

    return any(_test(d) for d in range(2, 1 + b // 2))


def prog_opt(debug=True):
    b_ini, c = (79, 79) if debug else (107_900, 124_900)
    return sum(1 for b in range(b_ini, c + 1, 17) if f_test(b))


def main(data: str):
    program = read_program(data.splitlines())
    yield run_program(program, debug=True)
    yield prog_opt(debug=False)
