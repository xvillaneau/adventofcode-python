
from libaoc import simple_main
from libaoc.files import read_full

def parse_instructions(instructions: str):
    char_map = {"(": 1, ")": -1}
    yield from map(char_map.__getitem__, instructions.strip())

def count_floors(instructions: str) -> int:
    return sum(parse_instructions(instructions))

def basement_first(instructions: str) -> int:
    pos = 0
    for i, move in enumerate(parse_instructions(instructions)):
        pos += move
        if pos == -1:
            return i+1

if __name__ == '__main__':
    simple_main(2015, 1, read_full, count_floors, basement_first)
