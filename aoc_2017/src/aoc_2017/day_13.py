import re
from typing import List, Dict

Filters = Dict[int, int]


def parse_file(lines: List[str]) -> Filters:
    re_line = re.compile(r"^(\d+): (\d+)$")
    parsed = (re_line.match(line).groups() for line in lines if line.strip())
    return dict((int(a), int(b)) for a, b in parsed)


def scan_hit(depth: int, scan_range: int, delay: int = 0) -> bool:
    index = depth + delay
    freq = (scan_range - 1) * 2
    return index % freq == 0


def count_hits(filters, delay=0):
    return sum(scan_hit(d, r, delay) for d, r in filters.items())


def severity(filters: Filters):

    def _sev(depth, scan_range):
        return int(scan_hit(depth, scan_range)) * depth * scan_range

    return sum(_sev(d, r) for d, r in filters.items())


def first_pass(filters: Filters):
    delay = 0
    while True:
        if count_hits(filters, delay) == 0:
            yield delay
        delay += 1


def main(data: str):
    big_file = parse_file(data.splitlines())
    yield severity(big_file)
    yield next(first_pass(big_file))
