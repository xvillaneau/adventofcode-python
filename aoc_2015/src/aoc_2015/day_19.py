from functools import partial
import random
import re

from libaoc.algo import AStarSearch

def parse_input(data: str, reverse=False):
    repl_lines, molecule = data.split('\n\n')
    replacements = []
    for line in repl_lines.strip().splitlines():
        pattern, replace = line.split(' => ')
        if reverse:
            pattern, replace = replace, pattern
        replacements.append((re.compile(pattern), replace))
    return replacements, molecule.strip()

def possible_replacements(molecule: str, pattern, replacement: str):
    for match in pattern.finditer(molecule):
        start, end = match.span()
        yield molecule[:start] + replacement + molecule[end:]

def all_replacements(replacements, molecule):
    return set(
        res
        for pattern, replace in replacements
        for res in possible_replacements(molecule, pattern, replace)
    )

def rand_replacements(replacements, molecule):
    results = [
        res
        for pattern, replace in replacements
        for res in possible_replacements(molecule, pattern, replace)
    ]
    random.shuffle(results)
    return results

def part_1(data: str):
    return len(all_replacements(*parse_input(data)))

def fewest_transforms(replacements, molecule):
    result = AStarSearch(molecule, 'e'.__eq__, partial(rand_replacements, replacements), len)
    return result.search().path()

def part_2(data):
    return len(fewest_transforms(*parse_input(data, reverse=True))) - 1


def main(data: str):
    yield part_1(data)
    yield part_2(data)
