from typing import List, Tuple
import re
import numpy as np

RE_CLAIM = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
Claim = Tuple[int, slice, slice]


def parse_claim(line: str) -> Claim:
    n, x0, y0, dx, dy = RE_CLAIM.fullmatch(line).groups()
    slice_x = slice(x0 := int(x0), x0 + int(dx))
    slice_y = slice(y0 := int(y0), y0 + int(dy))
    return n, slice_x, slice_y


def overlap_claims(claims: List[Claim], dim=(1000, 1000)):
    fabric = np.zeros(dim, dtype=int)
    for _, sx, sy in claims:
        fabric[sx, sy] += 1
    return fabric


def main(data: str):
    claims = [parse_claim(line) for line in data.splitlines()]
    overlap = overlap_claims(claims)
    yield np.sum(overlap >= 2)
    yield next(n for n, sx, sy in claims if np.all(overlap[sx, sy] == 1))
