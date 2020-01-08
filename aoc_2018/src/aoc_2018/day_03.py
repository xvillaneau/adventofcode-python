
from typing import Tuple
import re
import numpy as np
from libaoc import simple_main, files

RE_CLAIM = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
Claim = Tuple[int, int, int, int, int]

TEST = ['#1 @ 1,3: 4x4',
        '#2 @ 3,1: 4x4',
        '#3 @ 5,5: 2x2']


def parse_claim(line) -> Tuple[int, int, int, int, int]:
    match = RE_CLAIM.search(line)
    if not match:
        raise ValueError(line)
    return tuple(map(int, match.groups()))


def claim_to_mat(claim: Claim, max_x=1000, max_y=1000):
    _, off_x, off_y, dim_x, dim_y = claim
    ones = np.ones((dim_x, dim_y))
    return np.pad(ones, ((off_x, max_x - off_x - dim_x), (off_y, max_y - off_y - dim_y)), 'constant')


def pos_in_claim(pos: Tuple[int, int], claim: Claim):
    _, off_x, off_y, dim_x, dim_y = claim
    x, y = pos
    return off_x <= x < off_x + dim_x and off_y <= y < off_y + dim_y


def count_overlap(claims_text, dim_x=1000, dim_y=1000):
    claims = list(parse_claim(l) for l in claims_text)
    claim_mats = {c[0]: claim_to_mat(c, dim_x, dim_y) for c in claims}
    overlaps = sum(claim_mats.values()) >= 2

    intact_id = object()
    for c_id, c_mat in claim_mats.items():
        if not (c_mat * overlaps).any():
            intact_id = c_id
            break

    return overlaps.sum(), intact_id


if __name__ == '__main__':
    simple_main(2018, 3, files.read_lines, count_overlap, lambda _: '')
