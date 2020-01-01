from dataclasses import dataclass
from typing import List


@dataclass
class Registers:
    a: int = 0
    b: int = 0

    def half_a(self):
        self.a //= 2

    def half_b(self):
        self.b //= 2

    def triple_a(self):
        self.a *= 3

    def triple_b(self):
        self.b *= 3

    def incr_a(self):
        self.a += 1

    def incr_b(self):
        self.b += 1

    def jump(self, offset: int) -> int:
        return offset

    def jump_even_a(self, offset: int) -> int:
        return 1 if self.a % 2 else offset

    def jump_even_b(self, offset) -> int:
        return 1 if self.b % 2 else offset

    def jump_odd_a(self, offset) -> int:
        return offset if self.a == 1 else 1

    def jump_odd_b(self, offset) -> int:
        return offset if self.b == 1 else 1

STATIC_INSTR = {
    "hlf a": Registers.half_a,
    "hlf b": Registers.half_b,
    "tpl a": Registers.triple_a,
    "tpl b": Registers.triple_b,
    "inc a": Registers.incr_a,
    "inc b": Registers.incr_b,
}
OFFSET_INSTR = {
    "jie a,": Registers.jump_even_a,
    "jie b,": Registers.jump_even_b,
    "jio a,": Registers.jump_odd_a,
    "jio b,": Registers.jump_odd_b,
}

def parse_code(code: List[str]):
    res = []
    for line in code:
        if line in STATIC_INSTR:
            res.append((STATIC_INSTR[line],))
        elif line.startswith("jmp"):
            offset = int(line[3:])
            res.append((Registers.jump, offset))
        elif line[:3] in ('jie', 'jio'):
            offset = int(line[6:])
            res.append((OFFSET_INSTR[line[:6]], offset))
        else:
            raise ValueError(f"Invalid line: {line!r}")
    return res

def run(code, **init):
    ops = parse_code(code)
    pointer, regs = 0, Registers(**init)
    while 0 <= pointer < len(ops):
        op, *args = ops[pointer]
        res = op(regs, *args)
        assert res != 0
        pointer += 1 if res is None else res
    return regs

if __name__ == '__main__':
    from libaoc import simple_main, files
    from functools import partial
    part_1, part_2 = run, partial(run, a=1)
    simple_main(2015, 23, files.read_lines, part_1, part_2)
