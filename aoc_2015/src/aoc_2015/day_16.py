from operator import eq, gt, lt
import re

RE_SUE = re.compile(r"Sue (\d+):")
RE_PROPERTIES = re.compile(r"(\w+): (\d+),?")

def parse_sues(list_sues):
    for line in list_sues:
        num = int(RE_SUE.match(line).group(1))
        props = [
            (thing, int(value))
            for thing, value in RE_PROPERTIES.findall(line)
        ]
        yield num, props

READINGS = {
    "children": (3, eq),
    "cats": (7, gt),
    "samoyeds": (2, eq),
    "pomeranians": (3, lt),
    "akitas": (0, eq),
    "vizslas": (0, eq),
    "goldfish": (5, lt),
    "trees": (3, gt),
    "cars": (2, eq),
    "perfumes": (1, eq),
}

def find_sue(list_sues):
    for num, things in parse_sues(list_sues):
        if any(READINGS[k][0] != v for k, v in things):
            continue
        return num

def find_sue_2(list_sues):
    for num, things in parse_sues(list_sues):
        for k, v in things:
            read, func = READINGS[k]
            if not func(v, read):
                break
        else:
            return num


def main(data: str):
    aunts = data.splitlines()
    yield find_sue(aunts)
    yield find_sue_2(aunts)
