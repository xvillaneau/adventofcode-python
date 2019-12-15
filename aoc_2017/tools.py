
import numpy as np
import os
from typing import List

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')


def data_path(name):
    return os.path.join(DATA_DIR, name)


def read_full(name) -> str:
    with open(data_path(name)) as f:
        return f.read()


def read_lines(name) -> List[str]:
    return read_full(name).splitlines()


def read_int(name) -> int:
    raw = read_full(name)
    return int(raw.strip())


def read_int_table(name, delimiter=' '):
    return np.loadtxt(data_path(name), dtype=int, delimiter=delimiter)


def read_int_list(name, delimiter=' '):
    table = read_int_table(name, delimiter)
    return list(int(i) for i in table)
