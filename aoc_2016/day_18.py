from collections.abc import Iterator
from itertools import count, islice

TRAP_PARENTS = {"^^.", ".^^", "^..", "..^"}

class Row(Iterator):
    def __init__(self, first_row: str):
        self.row = [True] + [c == "." for c in first_row] + [True]
        self._ini = True

    def __next__(self):
        if self._ini:
            self._ini = False
            return sum(self.row) - 2
        safe_count, buffer = 0, True
        for i in range(1, len(self.row) - 1):
            safe = (self.row[i + 1] == buffer)
            safe_count += safe
            buffer, self.row[i] = self.row[i], safe
        return safe_count

def next_row(row: str):
    row, res = "." + row + ".", ""
    for i in range(len(row) - 2):
        res += "." if row[i] == row[i+2] else "^"
    return res

def count_safe_tiles(first_row: str, depth=40):
    row_iter = Row(first_row)
    return sum(islice(row_iter, depth))

if __name__ == '__main__':
    from functools import partial
    from libaoc import simple_main, files
    simple_main(
        2016,
        18,
        files.read_full,
        count_safe_tiles,
        partial(count_safe_tiles, depth=400_000),
    )
