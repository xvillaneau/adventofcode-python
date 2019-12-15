from collections import defaultdict
from functools import partial
from typing import Callable, Dict, List, Tuple, Union

Register = Dict[str, int]
Queue = List[int]
Pointer = int
Input = Union[int, str]
Context = Tuple[Register, Pointer, Queue]
Operation = Callable[[Context], Context]
Program = List[Tuple[str, Operation]]


class RecoveredFreq(Exception):

    def __init__(self, freq: int):
        Exception.__init__(self)
        self.freq = freq


class WaitForDuet(Exception):
    pass


def op_snd(val: Input, context: Context) -> Context:
    """Sound a frequency: set the last sounded to that freq"""
    regs, pos, queue = context
    new_queue = queue.copy()
    new_queue.append(val if isinstance(val, int) else regs[val])
    return regs, pos + 1, new_queue


def op_set(address: str, val: Input, context: Context) -> Context:
    """Set a register to a given value"""
    regs, pos, queue = context
    new_regs = regs.copy()
    new_regs[address] = val if isinstance(val, int) else regs[val]
    return new_regs, pos + 1, queue


def op_add(address: str, val: Input, context: Context) -> Context:
    """Add a value to a register"""
    regs, pos, queue = context
    new_regs = regs.copy()
    new_regs[address] += val if isinstance(val, int) else regs[val]
    return new_regs, pos + 1, queue


def op_mul(address: str, val: Input, context: Context) -> Context:
    """Multiply a register by a value"""
    regs, pos, queue = context
    new_regs = regs.copy()
    new_regs[address] *= val if isinstance(val, int) else regs[val]
    return new_regs, pos + 1, queue


def op_mod(address: str, val: Input, context: Context) -> Context:
    """Add a value to a register"""
    regs, pos, queue = context
    new_regs = regs.copy()
    new_regs[address] %= val if isinstance(val, int) else regs[val]
    return new_regs, pos + 1, queue


def op_rcv(val: Input, context: Context) -> Context:
    regs, pos, queue = context
    test = val if isinstance(val, int) else regs[val]
    if test != 0:
        if not queue:
            raise ValueError("No frequency played yet")
        raise RecoveredFreq(queue[-1])
    return regs, pos + 1, queue


def op_rcv_duet(address: str, context: Context) -> Context:
    regs, pos, queue = context
    if not queue:
        raise WaitForDuet
    new_regs = regs.copy()
    new_regs[address] = queue[0]
    return new_regs, pos + 1, queue[1:]


def op_jgz(val: Input, jump: Input, context: Context) -> Context:
    regs, pos, last = context
    test = val if isinstance(val, int) else regs[val]
    jump = jump if isinstance(jump, int) else regs[jump]

    if test <= 0:
        return regs, pos + 1, last
    if jump == 0:
        raise ValueError("Infinite loop entered!")
    return regs, pos + jump, last


def read_file(contents: List[str], duet=False) -> Program:

    ops_addr_val = {'set': op_set, 'add': op_add, 'mul': op_mul, 'mod': op_mod}

    def _to_input(string: str) -> Input:
        try:
            return int(string)
        except ValueError:
            return string

    def _line_to_op(line: str) -> Tuple[str, Operation]:
        elems = line.split()
        op = elems[0]

        if op in ops_addr_val:
            address, val = elems[1], _to_input(elems[2])
            f_op = partial(ops_addr_val[op], address, val)

        elif op == 'snd':
            val = _to_input(elems[1])
            f_op = partial(op_snd, val)

        elif op == 'rcv':
            if duet:
                address = elems[1]
                f_op = partial(op_rcv_duet, address)
            else:
                val = _to_input(elems[1])
                f_op = partial(op_rcv, val)

        elif op == 'jgz':
            val, jump = _to_input(elems[1]), _to_input(elems[2])
            f_op = partial(op_jgz, val, jump)

        else:
            raise ValueError(f"Invalid operation: {op}")

        return op, f_op

    return [_line_to_op(line) for line in contents if line.strip()]


def run_single(program: Program):

    queue, pos = [], 0
    registers = defaultdict(int)

    while True:
        _, op = program[pos]
        registers, pos, queue = op((registers, pos, queue))


def run_duet(program: Program):

    reg0, reg1 = defaultdict(int), defaultdict(int)
    reg1['p'] = 1
    q0, q1, p0, p1 = [], [], 0, 0
    count_snd_1 = 0

    while True:

        # Program 0
        locked_0 = False
        name, op = program[p0]
        try:
            if name == 'snd':
                reg0, p0, q1 = op((reg0, p0, q1))
            else:
                reg0, p0, q0 = op((reg0, p0, q0))
        except WaitForDuet:
            locked_0 = True

        # Program 1
        name, op = program[p1]
        try:
            if name == 'snd':
                reg1, p1, q0 = op((reg1, p1, q0))
                count_snd_1 += 1
            else:
                reg1, p1, q1 = op((reg1, p1, q1))
        except WaitForDuet:
            if locked_0:
                return count_snd_1


def day_18(lines: List[str]):
    program = read_file(lines)
    try:
        run_single(program)
    except RecoveredFreq as ex:
        yield ex.freq

    dual_program = read_file(lines, duet=True)
    yield run_duet(dual_program)


if __name__ == '__main__':
    from libaoc import iter_main, files
    iter_main(2017, 18, files.read_lines, day_18)
