from itertools import islice
from typing import Generator, List, Tuple
import numpy as np

START = '.#./..#/###'


class Pattern(object):

    def __init__(self, pattern: str):

        str_lines = pattern.split('/')
        lists = [[c == "#" for c in l] for l in str_lines]
        self.mat = np.array(lists, bool)

        self.size = self.mat.shape[0]
        assert self.size == self.mat.shape[1]  # Is a square

    def __contains__(self, item: 'Pattern') -> bool:

        if not self.size == item.size:
            raise ValueError("Can only match patterns of same size")

        flip = self.mat.T

        def _rotations(m):
            for i in range(4):
                yield np.rot90(m, i)

        return (any((item.mat == m).all() for m in _rotations(self.mat))
                or any((item.mat == m).all() for m in _rotations(flip)))

    def __eq__(self, other: 'Pattern'):
        return (self.mat == other.mat).all()

    def __str__(self):

        def _char(b: bool) -> str:
            return '#' if b else '.'

        lines = [''.join(_char(b) for b in l) for l in self.mat]
        return '/'.join(lines)

    def __repr__(self):
        return f'<Pattern {self}>'

    @classmethod
    def assemble(cls, parts: List['Pattern'], size: int) -> 'Pattern':
        r = range(size)
        lines = [np.concatenate([parts[j].mat for j in range(i, i + size)], axis=1)
                 for i in range(0, size ** 2, size)]
        mat = np.concatenate(lines)
        return cls.from_array(mat)

    @classmethod
    def from_array(cls, array: np.ndarray) -> 'Pattern':

        assert array.dtype == 'bool'
        assert array.ndim == 2
        size = array.shape[0]
        assert size == array.shape[1]

        pattern = cls('#')
        pattern.mat = array
        pattern.size = size
        return pattern

    def split(self) -> Tuple[List['Pattern'], int]:

        if not self.size % 2:
            k = 2
        elif not self.size % 3:
            k = 3
        else:
            raise ValueError(f"Unsupported split size {self.size}")

        r = range(0, self.size, k)
        ids = [(list(range(i, i + k)), list(range(j, j + k))) for i in r for j in r]
        mats = [self.mat[np.ix_(rx, ry)] for rx, ry in ids]
        return [self.from_array(m) for m in mats], self.size // k


Rule = Tuple[Pattern, Pattern]
RuleSet = Tuple[List[Rule], List[Rule]]


def read_rule(rule: str) -> Rule:
    bits = rule.split(' => ')
    match, result = Pattern(bits[0]), Pattern(bits[1])
    assert match.size in (2, 3)
    assert result.size == match.size + 1
    return match, result


def read_all_rules(lines: List[str]) -> RuleSet:
    rules_2, rules_3 = [], []

    for l in lines:
        pats = read_rule(l)
        if pats[0].size == 2:
            rules_2.append(pats)
        else:
            rules_3.append(pats)

    return rules_2, rules_3


def match_rule(pattern: Pattern, rules: RuleSet) -> Pattern:
    sized_rules = rules[0] if pattern.size == 2 else rules[1]
    return next(res for match, res in sized_rules if pattern in match)


def fractal_art(rules: RuleSet) -> Generator[Pattern, None, None]:
    pattern = Pattern(START)

    while True:
        old_bits, size = pattern.split()
        new_bits = [match_rule(p, rules) for p in old_bits]
        pattern = Pattern.assemble(new_bits, size)
        yield pattern


def fractal_count_iter(rules: RuleSet, n: int) -> int:
    gen = fractal_art(rules)
    pattern = next(islice(gen, n - 1, n))
    return pattern.mat.sum()


def day_21(lines: List[str]):
    rules = read_all_rules(lines)
    yield fractal_count_iter(rules, 5)
    # TODO: This is SLOW
    yield fractal_count_iter(rules, 18)


if __name__ == '__main__':
    from libaoc import iter_main, files
    iter_main(2017, 21, files.read_lines, day_21)
