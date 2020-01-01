import operator
import re
from typing import Dict, Iterable, List

RE_LINE = re.compile(r'^(.*) -> (\w+)$')
OPERATIONS = {'AND', 'OR', 'NOT', 'RSHIFT', 'LSHIFT'}
B16 = (1 << 16) - 1

class Gates:
    _ops = {
        "AND": operator.and_,
        "OR": operator.or_,
        "RSHIFT": operator.rshift,
        "LSHIFT": operator.lshift,
    }

    def __init__(self, instructions: Iterable[str]):
        self.wires: Dict[str, str] = {}
        for line in instructions:
            if match := RE_LINE.match(line):
                gate, wire = match.groups()
                self.wires[wire] = gate

    def __iter__(self):
        for wire in self.wires:
            yield wire, self.get_value(wire)

    def get_value(self, wire: str):
        try:
            return int(wire)
        except ValueError:
            pass

        val = self.wires[wire]
        if isinstance(val, int):
            return val

        bits = val.split()
        if len(bits) == 1:
            res = self.get_value(bits[0])

        elif len(bits) == 2:
            op, x = bits
            assert op == "NOT", f"Invalid line: {val}"
            x = self.get_value(x)
            res = B16 ^ x

        elif len(bits) == 3:
            x, op, y = bits
            x = self.get_value(x)
            y = self.get_value(y)
            res = self._ops[op](x, y) & B16

        else:
            raise ValueError(f"Invalid line: {val}")

        self.wires[wire] = res
        return res

def solve_gates(instructions: List[str]):
    _instr = list(instructions)
    gates_1 = Gates(_instr)
    res_1 = gates_1.get_value("a")
    gates_2 = Gates(_instr + [f"{res_1} -> b"])
    res_2 = gates_2.get_value("a")
    return res_1, res_2

def test_connect_wires():
    from textwrap import dedent
    instr = dedent("""
        x AND y -> d
        x OR y -> e
        x LSHIFT 2 -> f
        y RSHIFT 2 -> g
        NOT x -> h
        NOT y -> i
        123 -> x
        456 -> y
        """).strip().splitlines()

    gates = Gates(instr)
    print(dict(gates))


if __name__ == '__main__':
    from libaoc import files, tuple_main
    tuple_main(2015, 7, files.read_lines, solve_gates)
