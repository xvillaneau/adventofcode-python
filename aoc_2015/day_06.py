from array import array
import re
from typing import NamedTuple

class Position(NamedTuple):
    x: int
    y: int

class LampGrid:

    RE_INSTRUCTION = re.compile(r"^(.*) (\d+),(\d+) through (\d+),(\d+)$")

    def __init__(self, length: int, width: int):
        self.l, self.w = length, width
        self._mem = array('B', [0] * (length * width))

    def __str__(self):
        res = ""
        for x in range(0, self.w * self.l, self.l):
            line = self._mem[x:x+self.l].tolist()
            res += ''.join(map(("-", "*").__getitem__, line)) + "\n"
        return res

    @staticmethod
    def _prep_corners(c1: Position, c2: Position):
        if c1.x > c2.x:
            c1, c2 = Position(c2.x, c1.y), Position(c1.x, c2.y)
        if c1.y > c2.y:
            c1, c2 = Position(c1.x, c2.y), Position(c2.x, c1.y)
        return c1, c2

    def _edit_range(self, start, end, operation):
        start, end = self._prep_corners(start, end)
        for x in range(start.x, end.x + 1):
            s, e = x * self.l + start.y, x * self.l + end.y + 1
            self._mem[s:e] = array('B', operation(self._mem[s:e]))

    def turn_on(self, start: Position, end: Position):
        self._edit_range(start, end, self._turn_on)

    def turn_off(self, start: Position, end: Position):
        self._edit_range(start, end, self._turn_off)

    def toggle(self, start: Position, end: Position):
        self._edit_range(start, end, self._toggle)

    @staticmethod
    def _turn_on(_array):
        return [1] * len(_array)

    @staticmethod
    def _turn_off(_array):
        return [0] * len(_array)

    @staticmethod
    def _toggle(_array):
        return [not x for x in _array.tolist()]

    def run_instruction(self, instruction: str):
        op, x1, y1, x2, y2 = self.RE_INSTRUCTION.match(instruction).groups()
        c1, c2 = Position(int(x1), int(y1)), Position(int(x2), int(y2))
        if op == "turn on":
            self.turn_on(c1, c2)
        elif op == "turn off":
            self.turn_off(c1, c2)
        elif op == "toggle":
            self.toggle(c1, c2)

    def count_lights(self):
        return sum(self._mem)


class ControllableLampGrid(LampGrid):

    @staticmethod
    def _turn_on(arr):
        return [x+1 for x in arr]

    @staticmethod
    def _turn_off(arr):
        return [max(0, x-1) for x in arr]

    @staticmethod
    def _toggle(arr):
        return [x+2 for x in arr]

def run(instructions, dim=(1000, 1000)):
    lamps_1 = LampGrid(*dim)
    lamps_2 = ControllableLampGrid(*dim)
    for l in instructions:
        lamps_1.run_instruction(l)
        lamps_2.run_instruction(l)
    return lamps_1.count_lights(), lamps_2.count_lights()

def test_lights():
    instr = [
        "turn on 0,0 through 2,2",
        "turn off 3,1 through 1,3",
        "toggle 2,3 through 0,1",
    ]
    assert run(instr, (4, 4)) == 10


if __name__ == '__main__':
    from libaoc import tuple_main, files
    tuple_main(2015, 6, files.read_lines, run)
