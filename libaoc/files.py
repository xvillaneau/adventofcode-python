from pathlib import Path
from typing import List

import numpy as np

ROOT_DIT = Path(__file__).parent.parent

def data_path(year: int, day: int):
    return ROOT_DIT / f'data_{year}' / f'day_{day:02}.txt'


def read_full(year: int, day: int) -> str:
    with open(data_path(year, day)) as f:
        return f.read()


def read_lines(year: int, day: int) -> List[str]:
    return read_full(year, day).strip().splitlines()


def read_int(year: int, day: int) -> int:
    return int(read_full(year, day))


def read_int_table(year: int, day: int, delimiter=None) -> np.ndarray:
    lines = read_lines(year, day)
    return np.array([[int(i) for i in line.split(delimiter)] for line in lines])


def read_int_list(year: int, day: int, delimiter=None):
    lines = read_lines(year, day)
    if len(lines) == 1:  # Assume it's a single line of ints
        return [int(i) for i in lines[0].split(delimiter)]
    else:  # Assume it's one int per line
        return [int(i) for i in lines]
