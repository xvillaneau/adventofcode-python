from typing import Tuple


def parse_box(line: str) -> Tuple[int, int, int]:
    l, w, h = line.split('x')
    return int(l), int(w), int(h)


def paper_required(length: int, height: int, width: int):
    sides = [length * width, width * height, height * length]
    return 2 * sum(sides) + min(sides)


def ribbon_required(length: int, height: int, width: int):
    perimeters = [length + width, width + height, height + length]
    return 2 * min(perimeters) + length * width * height


def main(data: str):
    boxes = data.splitlines()
    paper, ribbon = 0, 0
    for box in boxes:
        dimensions = parse_box(box)
        paper += paper_required(*dimensions)
        ribbon += ribbon_required(*dimensions)
    yield paper
    yield ribbon
