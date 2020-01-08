from dataclasses import dataclass
from typing import List, Callable, Dict, Iterable, FrozenSet, Tuple, Set
from parsimonious import Grammar


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


@dataclass
class RawOp:
    op_num: int
    reg_a: int
    reg_b: int
    reg_c: int


@dataclass
class OpExample:
    before: List[int]
    after: List[int]
    raw_op: RawOp


def parse_input(full_input: str):

    input_grammar = Grammar("""
    input        = example* instruction*
    example      = before instruction after
    before       = "Before: " state _
    after        = "After:  " state _
    instruction  = OPNUM _ VALUE _ VALUE _ VALUE _
    state        = "[" VALUE ", " VALUE ", " VALUE ", " VALUE "]"

    _     = ~"\s+"
    VALUE = ~"[0-9]"
    OPNUM = ~"[0-9]+"
    """)

    def _parse_state(state_tree):
        return [int(state_tree.children[i].text) for i in (1, 3, 5, 7)]

    def _parse_instruction(instruction_tree):
        values = [int(instruction_tree.children[i].text) for i in (0, 2, 4, 6)]
        return RawOp(*values)

    def _parse_example(example_tree):
        before = _parse_state(example_tree.children[0].children[1])
        operation = _parse_instruction(example_tree.children[1])
        after = _parse_state(example_tree.children[2].children[1])
        return OpExample(before, after, operation)

    tree = input_grammar.parse(full_input)
    examples = [_parse_example(ex) for ex in tree.children[0].children]
    program = [_parse_instruction(op) for op in tree.children[1].children]
    return examples, program


def try_example(example: OpExample):

    def _op_matches(op: Operation):
        reg = example.before.copy()
        op(example.raw_op.reg_a, example.raw_op.reg_b, example.raw_op.reg_c, reg)
        return reg == example.after

    return frozenset(name for name, op in OPERATIONS.items() if _op_matches(op))


def match_opcodes(matches: Iterable[Tuple[int, FrozenSet[str]]]) -> List[Operation]:
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
    for op in program:
        op_array[op.op_num](op.reg_a, op.reg_b, op.reg_c, registers)
    return registers


def main(data: str):
    examples, program = parse_input(data)
    matches = [(ex.raw_op.op_num, try_example(ex)) for ex in examples]
    yield sum(len(m) >= 3 for _, m in matches)
    result = run_program(program, match_opcodes(set(matches)))
    yield result[0]
