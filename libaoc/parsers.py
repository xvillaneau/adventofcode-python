"""
libaoc.parsers - Common data parsers for Advent of Code.

Basically, anything that we commonly use to convert text into usable
information has its place here. Replaces libaoc.files.
"""


def parse_lines(data: str):
    return data.strip().splitlines()


def parse_integer_list(data: str, delimiter=None):
    lines = parse_lines(data)
    if len(lines) == 1:  # Assume it's a single line of ints
        return [int(i) for i in lines[0].split(delimiter)]
    else:  # Assume it's one int per line
        return [int(i) for i in lines]
