from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Vect2D:
    x: int
    y: int

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, tuple):
            # Hash of a given Vect2D is equal to that of the tuple of
            # its coordinates, therefore we MUST implement equality too
            return (self.x, self.y) == other
        if isinstance(other, Vect2D):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __neg__(self):
        return self * -1

    def __mul__(self, other: int):
        return type(self)(self.x * other, self.y * other)

    def __rmul__(self, other: int):
        return self * other

    def __add__(self, other: 'Vect2D'):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vect2D'):
        return self + (-other)

    def __floordiv__(self, other: int):
        if not isinstance(other, int):
            return NotImplemented
        if self.x % other or self.y % other:
            raise ValueError("Can only divide a vector integrally")
        return type(self)(self.x // other, self.y // other)

    def __invert__(self):
        return type(self)(self.y, self.x)

    def __complex__(self):
        return self.x + self.y * 1j

    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def __lt__(self, other):
        return self.x + self.y < other.x + other.y

    def up(self):
        return self + UP

    def down(self):
        return self + DOWN

    def left(self):
        return self + LEFT

    def right(self):
        return self + RIGHT


ORIGIN = Vect2D(0, 0)
UP, DOWN = Vect2D(0, 1), Vect2D(0, -1)
LEFT, RIGHT = Vect2D(-1, 0), Vect2D(1, 0)
UNIT_VECTORS = [UP, RIGHT, DOWN, LEFT]


class Direction(Enum):
    Left = LEFT
    Up = UP
    Right = RIGHT
    Down = DOWN

    def __new__(cls, vector: Vect2D):
        obj = object.__new__(cls)
        obj._value_ = len(cls.__members__)
        obj.vector = vector
        return obj

    @property
    def left(self):
        return Direction((self.value - 1) & 3)

    @property
    def right(self):
        return Direction((self.value + 1) & 3)


class Instruction(Enum):
    Left = 'L'
    Right = 'R'
    Move = 'M'


class Walker2D:

    def __init__(self, x: int, y: int, direction: Direction):
        self.pos = Vect2D(x, y)
        self.direction = direction

    def rot_left(self):
        self.direction = self.direction.left

    def rot_right(self):
        self.direction = self.direction.right

    def move(self, n_steps: int = 1):
        self.pos += self.direction.vector * n_steps

    def do(self, instruction: Instruction):
        if instruction == Instruction.Left:
            self.rot_left()
        elif instruction == Instruction.Right:
            self.rot_right()
        elif instruction == Instruction.Move:
            self.move()


@dataclass(frozen=True)
class StaticWalker:
    pos: Vect2D
    direction: Direction

    def rot_left(self):
        return StaticWalker(self.pos, self.direction.left)

    def rot_right(self):
        return StaticWalker(self.pos, self.direction.right)

    def move(self, n_step: int = 1):
        move = self.direction.vector * n_step
        return StaticWalker(self.pos + move, self.direction)
