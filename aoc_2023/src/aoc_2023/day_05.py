import bisect
import itertools


class Mapper:

    def __init__(self, mappings: list[str]):
        self._src: list[int] = []
        self._dst: list[int] = []
        self._ranges: list[int] = []

        def parse_line(_ln: str) -> tuple[int, int, int]:
            d, s, n = (int(n) for n in _ln.split())
            return d, s, n

        for line in mappings:
            dst, src, rg = parse_line(line)
            i = bisect.bisect(self._src, src)
            self._src.insert(i, src)
            self._dst.insert(i, dst)
            self._ranges.insert(i, rg)

    def __getitem__(self, num: int) -> int:
        i = bisect.bisect_right(self._src, num)
        if i == 0:
            return num
        src = self._src[i-1]
        dst = self._dst[i-1]
        rg = self._ranges[i-1]
        if num < src + rg:
            return dst + num - src
        return num

    def map_range(self, start: int, end: int) -> list[tuple[int, int]]:
        """
        map_range computes the destination values for an entire range
        of numbers, returning a list of ranges.
        """
        if end <= start:
            return []

        i = bisect.bisect_right(self._src, start)
        if i > 0:
            # Check if start of range is within a source mapping range
            src = self._src[i-1]
            dst = self._dst[i-1]
            rg = self._ranges[i-1]
            offset = dst - src

            if end <= src + rg:
                # Range entirely contained in source range
                return [(offset + start, offset + end)]
            if start < src + rg:
                # Range partly in source range, map the first part and process the rest
                return [(offset + start, dst + rg), *self.map_range(src + rg, end)]

        if i < len(self._src):
            # Check if the end of the range extends beyond the next source range
            nxt = self._src[i]
            if end > nxt:
                return [(start, nxt), *self.map_range(nxt, end)]

        return [(start, end)]


def parse_data(data: str):
    blocks = data.strip().split("\n\n")
    if not blocks[0].startswith("seeds: "):
        raise ValueError("Expecting seeds list at the start")
    seeds = [int(n) for n in blocks[0].split()[1:]]

    mappers: list[Mapper] = []
    for block in blocks[1:]:
        lines = block.splitlines()
        mappers.append(Mapper(lines[1:]))

    return seeds, mappers


def get_location(start: int, length: int, mappers: list[Mapper]) -> int:
    ranges = [(start, start + length)]
    for mapper in mappers:
        new_ranges = []
        for beg, end in ranges:
            new_ranges.extend(mapper.map_range(beg, end))
        ranges = new_ranges
    return min(s for s, _ in ranges)


def main(data: str):
    seeds, mappers = parse_data(data)
    yield min(get_location(seed, 1, mappers) for seed in seeds)

    assert len(seeds) % 2 == 0
    yield min(
        get_location(start, ln, mappers)
        for start, ln in itertools.batched(seeds, 2)
    )
