import re
from typing import List, Callable, Dict, Iterable, Tuple, Set, NamedTuple


def add_register(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = registers[reg_a] + registers[reg_b]


def add_immediate(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = registers[reg_a] + reg_b


def multiply_register(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = registers[reg_a] * registers[reg_b]


def multiply_immediate(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = registers[reg_a] * reg_b


def bitwise_and_register(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = registers[reg_a] & registers[reg_b]


def bitwise_and_immediate(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = registers[reg_a] & reg_b


def bitwise_or_register(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = registers[reg_a] | registers[reg_b]


def bitwise_or_immediate(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = registers[reg_a] | reg_b


def set_register(reg_a, _, reg_c, registers):
    registers[reg_c] = registers[reg_a]


def set_immediate(reg_a, _, reg_c, registers):
    registers[reg_c] = reg_a


def greater_than_immediate_register(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = 1 if reg_a > registers[reg_b] else 0


def greater_than_register_immediate(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = 1 if registers[reg_a] > reg_b else 0


def greater_than_register_register(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = 1 if registers[reg_a] > registers[reg_b] else 0


def equal_immediate_register(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = 1 if reg_a == registers[reg_b] else 0


def equal_register_immediate(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = 1 if registers[reg_a] == reg_b else 0


def equal_register_register(reg_a, reg_b, reg_c, registers):
    registers[reg_c] = 1 if registers[reg_a] == registers[reg_b] else 0


Operation = Callable[[int, int, int, List[int]], None]
OPERATIONS: Dict[str, Operation] = {
    "addr": add_register,
    "addi": add_immediate,
    "mulr": multiply_register,
    "muli": multiply_immediate,
    "banr": bitwise_and_register,
    "bani": bitwise_and_immediate,
    "borr": bitwise_or_register,
    "bori": bitwise_or_immediate,
    "setr": set_register,
    "seti": set_immediate,
    "gtir": greater_than_immediate_register,
    "gtri": greater_than_register_immediate,
    "gtrr": greater_than_register_register,
    "eqir": equal_immediate_register,
    "eqri": equal_register_immediate,
    "eqrr": equal_register_register,
}


class RawOp(NamedTuple):
    op_num: int
    reg_a: int
    reg_b: int
    reg_c: int


class Example(NamedTuple):
    before: List[int]
    after: List[int]
    raw_op: RawOp


def parse_input(full_input: str):
    raw_examples, raw_program = full_input.split("\n\n\n\n")

    re_num = re.compile(r'\d+')
    def extract_nums(string: str):
        return list(map(int, re_num.findall(string)))

    examples = []
    for raw in raw_examples.split("\n\n"):
        before, op, after = raw.splitlines()
        examples.append(
            Example(
                extract_nums(before), extract_nums(after), RawOp(*extract_nums(op))
            )
        )

    program = [RawOp(*extract_nums(line)) for line in raw_program.splitlines()]
    return examples, program


def try_example(example: Example):
    before, after, (_, a, b, c) = example

    def _op_matches(op: Operation):
        reg = before.copy()
        op(a, b, c, reg)
        return reg == after

    return tuple(name for name, op in OPERATIONS.items() if _op_matches(op))


def match_opcodes(matches: Iterable[Tuple[int, Tuple[str]]]) -> List[Operation]:
    numbers = list(range(16))
    all_codes = set(OPERATIONS)
    tmp: Dict[int, Set[str]] = {num: all_codes.copy() for num in numbers}

    for num, codes in matches:
        tmp[num].intersection_update(codes)

    nums_to_code: Dict[int, str] = {}
    while len(nums_to_code) < 16:
        found_num = next(num for num, codes in tmp.items() if len(codes) == 1)
        found_code = tmp.pop(found_num).pop()
        nums_to_code[found_num] = found_code
        for codes in tmp.values():
            codes.difference_update({found_code})

    return [OPERATIONS[nums_to_code[n]] for n in numbers]


def run_program(program: List[RawOp], op_array: List[Operation]):
    registers = [0, 0, 0, 0]
    for op, a, b, c in program:
        op_array[op](a, b, c, registers)
    return registers


def main(data: str):
    examples, program = parse_input(data)
    matches = [(ex.raw_op.op_num, try_example(ex)) for ex in examples]
    yield sum(len(m) >= 3 for _, m in matches)
    result = run_program(program, match_opcodes(set(matches)))
    yield result[0]
