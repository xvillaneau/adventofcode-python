"""
libaoc.parsers - Common data parsers for Advent of Code.

Basically, anything that we commonly use to convert text into usable
information has its place here. Replaces libaoc.files.
"""
import numpy as np


def parse_integer_list(data: str, delimiter=None):
    lines = data.splitlines()
    if len(lines) == 1:  # Assume it's a single line of ints
        return [int(i) for i in lines[0].split(delimiter)]
    else:  # Assume it's one int per line
        return [int(i) for i in lines]


def parse_integer_table(data: str, delimiter=None):
    lines = data.splitlines()
    return np.array([[int(i) for i in line.split(delimiter)] for line in lines])
