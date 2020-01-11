from typing import List
from libaoc.vectors import Walker2D, Direction


TEST = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
"""


TEST_2 = r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
"""


CHR_DIR = {
    '^': Direction.Left,
    '>': Direction.Up,
    'v': Direction.Right,
    '<': Direction.Down
}
NEXT_LEFT, NEXT_STRAIGHT, NEXT_RIGHT = 0, 1, 2


class Cart(Walker2D):

    def __init__(self, x: int, y: int, direction: Direction):
        Walker2D.__init__(self, x, y, direction)
        self.crossing_status = NEXT_LEFT
        self.crashed = False

    def grid_move(self, grid_chr: str):
        if grid_chr == '+':
            if self.crossing_status == NEXT_LEFT:
                self.rot_left()
                self.crossing_status = NEXT_STRAIGHT
            elif self.crossing_status == NEXT_RIGHT:
                self.rot_right()
                self.crossing_status = NEXT_LEFT
            else:
                self.crossing_status = NEXT_RIGHT

        elif grid_chr in r'\/':
            if (self.direction in (Direction.Up, Direction.Down)) == (grid_chr == '/'):
                self.rot_left()
            else:
                self.rot_right()

        self.move()


def load_input(input_lines: List[str]):

    max_len = max(len(line) for line in input_lines)
    full_input = [line.ljust(max_len) for line in input_lines]

    carts = []
    for x, line in enumerate(full_input):
        for y, c in enumerate(line):
            if c not in '><v^':
                continue
            carts.append(Cart(x, y, CHR_DIR[c]))

    _trans_rm = str.maketrans("><^v", "--||")
    grid = [line.translate(_trans_rm) for line in full_input]
    return grid, carts


def tick(grid: List[str], carts: List[Cart]):

    carts_by_coord = list(sorted(carts, key=lambda c: c.pos))  # Evaluate order NOW
    for cart in carts_by_coord:
        if cart.crashed:
            continue
        x, y = cart.pos
        cart.grid_move(grid[x][y])
        for other in carts:
            if other is cart:
                continue
            if other.pos == cart.pos:
                other.crashed = cart.crashed = True


def first_collision(lines):
    grid, carts = load_input(lines)
    while all(not c.crashed for c in carts):
        tick(grid, carts)
    x, y = next(c for c in carts if c.crashed).pos
    return f'{y},{x}'


def last_remaining(lines):
    grid, carts = load_input(lines)
    while len(carts) > 1:
        tick(grid, carts)
        carts = [c for c in carts if not c.crashed]
    x, y = carts[0].pos
    return f'{y},{x}'


def main(data: str):
    lines = data.splitlines()
    yield first_collision(lines)
    yield last_remaining(lines)
