from typing import List, Dict, Tuple
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


class Cart(Walker2D):

    def __init__(self, x: int, y: int, direction: Direction):
        Walker2D.__init__(self, x, y, direction)
        self.crossing_status = 0
        self.crashed = False

    def grid_move(self, grid_chr: str):
        if grid_chr == '+':
            if self.crossing_status == 0:
                self.rot_left()
            elif self.crossing_status == 2:
                self.rot_right()
            self.crossing_status += 1
            self.crossing_status %= 3
        elif grid_chr in r'\/':
            if (self.direction in (Direction.Up, Direction.Down)) == (grid_chr == '/'):
                self.rot_left()
            else:
                self.rot_right()
        self.move()


def load_input(input_lines: List[str]):

    max_len = max(len(l) for l in input_lines)
    full_input = [l + ' ' * (max_len - len(l)) for l in input_lines if l]

    assert len(set(len(l) for l in full_input)) == 1
    assert all(c in r'-|/\+><v^ ' for l in full_input for c in l)

    carts = []
    for x, l in enumerate(full_input):
        for y, c in enumerate(l):
            if c not in '><v^':
                continue
            carts.append(Cart(x, y, CHR_DIR[c]))

    def rm_carts(line: str):
        return line.replace('>', '-').replace('<', '-').replace('^', '|').replace('v', '|')

    grid = [rm_carts(l) for l in full_input]
    return grid, carts


def tick(grid: List[str], carts: List[Cart]):

    carts_by_coord = list(sorted(carts, key=lambda c: c.pos))  # Evaluate order NOW
    for cart in carts_by_coord:
        if cart.crashed:
            continue
        x, y = cart.pos
        cart.grid_move(grid[x][y])
        crashes = [c for c in carts if c is not cart and c.pos == cart.pos and not c.crashed]
        if crashes:
            cart.crashed = True
            for c in crashes:
                c.crashed = True


def show_state(grid: List[str], carts: List[Cart]):

    carts_by_pos: Dict[Tuple[int, int], Cart] = {c.pos: c for c in carts if not c.crashed}

    for x, l in enumerate(grid):
        for y, c in enumerate(l):
            if (x, y) in carts_by_pos:
                cart_dir = carts_by_pos[(x, y)].direction
                pos_chr = next(s for s, d in CHR_DIR.items() if d == cart_dir)
            else:
                pos_chr = c
            print(pos_chr, end='')
        print('')


def first_collision(lines):
    grid, carts = load_input(lines)
    while True:
        tick(grid, carts)
        if any(c.crashed for c in carts):
            x, y = next(c for c in carts if c.crashed).pos
            return f'{y},{x}'


def last_remaining(lines):
    grid, carts = load_input(lines)
    while True:
        tick(grid, carts)
        if sum(not c.crashed for c in carts) == 1:
            x, y = next(c for c in carts if not c.crashed).pos
            return f'{y},{x}'


def main(data: str):
    lines = data.splitlines()
    yield first_collision(lines)
    yield last_remaining(lines)
