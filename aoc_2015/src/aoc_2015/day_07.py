from typing import Dict, Iterable

B16 = (1 << 16) - 1


class Gates:
    def __init__(self, instructions: Iterable[str]):
        self.values: Dict[str, int] = {}
        self.gates: Dict[str, str] = {}
        self.setup_gates(instructions)

    def setup_gates(self, instructions: Iterable[str]):
        for line in instructions:
            gate, wire = line.split(" -> ")
            self.gates[wire] = gate

    def __getitem__(self, wire: str):
        if wire not in self.values:
            self.values[wire] = self.compute(self.gates[wire])
        return self.values[wire]

    def compute(self, gate: str):
        words = gate.split()

        if len(words) == 1:
            try:
                return int(gate)
            except ValueError:
                return self[gate]

        if len(words) == 2:
            assert words[0] == "NOT"
            return B16 ^ self[words[1]]

        x, op, y = words
        x = 1 if x == "1" else self[x]
        if op == "AND":
            res = x & self[y]
        elif op == "OR":
            res = x | self[y]
        elif op == "RSHIFT":
            res = x >> int(y)
        elif op == "LSHIFT":
            res = x << int(y)
        else:
            raise ValueError(op)
        return res & B16


def main(data: str):
    gates = Gates(data.splitlines())
    yield gates["a"]

    gates.gates["b"] = str(gates["a"])
    gates.values = {}
    yield gates["a"]
