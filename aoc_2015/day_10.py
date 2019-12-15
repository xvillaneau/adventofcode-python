from collections import deque
from functools import wraps, lru_cache
from itertools import islice, tee, groupby
import re
from typing import List, Iterator

from hypothesis import given, assume, strategies as st

# Basic computation of Look and Say
RE_LNS = re.compile(r'(.)\1*')

def imperative_look_and_say(string: str):
    result, times = "", 1
    repeat, *tail = string + " "
    for char in tail:
        if char != repeat:
            result += str(times) + repeat
            times, repeat = 1, char
            continue
        times += 1
    return result

def _lns_replace(match):
    return str(len(match.group())) + match.groups()[0]

def regex_look_and_say(string: str):
    return RE_LNS.sub(_lns_replace, string)

def groupby_look_and_say(string: str):
    return ''.join(
        str(len(list(g))) + k
        for k, g in groupby(string)
    )

look_and_say = imperative_look_and_say

def naive_deep_look_and_say(string: str, depth: int):
    for _ in range(depth):
        string = look_and_say(string)
    return string

# Splitting a sequence
RE_ENDSPLIT = re.compile(r'[^2]22$')
RE_SPLITS = [
    re.compile(r'21([^1])(?!\1)'),
    re.compile(r'2111[^1]'),
    re.compile(r'23(?:$|([^3]){1,2}(?!\1))'),
    re.compile(r'2([^123])(?!\1)'),
    re.compile(r'[^123][123]'),
]

def split(string: str) -> List[str]:
    return list(_split(string))

def _split(string: str) -> str:
    if string == '22':
        yield string
    elif RE_ENDSPLIT.search(string):
        yield from _split(string[:-2])
        yield '22'
    else:
        for regex in RE_SPLITS:
            if match := regex.search(string):
                p = match.start() + 1
                yield from _split(string[:p])
                yield from _split(string[p:])
                return
        yield string

# Memoization code
@lru_cache(maxsize=None)
def memo_look_and_say(string: str) -> List[str]:
    return split(look_and_say(string))

# Main call, this one is much faster
def deep_look_and_say(string: str, depth: int) -> List[str]:
    if depth <= 0:
        return [string]
    # IMPORTANT: Split can only be applied to 2+ day-old strings!
    atoms = [look_and_say(string)]
    for _ in range(depth-1):
        next_atoms = []
        for string in atoms:
            next_atoms.extend(memo_look_and_say(string))
        atoms = next_atoms
    return atoms

def linked_look_and_say(string: str, depth: int):
    assert depth >= 1
    atoms = deque([look_and_say(string)])
    for _ in range(depth-1):
        steps = len(atoms)
        for _ in range(steps):
            atom = atoms.popleft()
            atoms.extend(memo_look_and_say(atom))
    return atoms

def iter_look_and_say(string: str, depth: int, top=True):
    if depth <= 0:
        yield string
    elif top:
        yield from iter_look_and_say(
            look_and_say(string), depth-1, False
        )
    else:
        for atom in memo_look_and_say(string):
            yield from iter_look_and_say(atom, depth-1, False)

# Length-only optimization
def parallel_iterator(generator_func):
    roots = {}

    @wraps(generator_func)
    def inner(key, *args, **kwargs):
        if key not in roots:
            roots[key] = generator_func(key, *args, **kwargs)
        iterator, roots[key] = tee(roots[key], 2)
        return iterator

    return inner

@parallel_iterator
def iter_lengths(string: str, at_top: bool = True) -> Iterator[int]:
    yield len(string)
    description = look_and_say(string)
    atoms = [description] if at_top else split(description)
    iterators = [iter_lengths(s, at_top=False) for s in atoms]
    while True:
        yield sum(next(i) for i in iterators)

def fast_length(string: str, depth: int) -> int:
    return next(islice(iter_lengths(string), depth, None))

# Tests

def test_split():
    assert split('22') == ['22']
    assert split('1113122113') == ['1113122113']
    assert split('311311222112') == ['311311222112']
    assert split('1113213211') == ['11132', '13211']
    assert split('121113223122') == ['12', '1113', '22', '31', '22']
    assert split('312211322212221121123222112') == ['312211322212221121123222112']
    assert split('31121123') == ['3112112', '3']

def test_part_1():
    assert look_and_say('1') == '11'
    assert look_and_say('11') == '21'
    assert look_and_say('21') == '1211'
    assert look_and_say('1211') == '111221'
    assert look_and_say('111221') == '312211'
    assert deep_look_and_say('1', 5) == ['312211']
    assert deep_look_and_say('3', 5) == ['1113122113']
    assert deep_look_and_say('41111', 5) == ['11222112', '3114', '111221']
    assert list(linked_look_and_say('3', 5)) == ['1113122113']
    assert list(linked_look_and_say('41111', 5)) == ['11222112', '3114', '111221']
    assert list(iter_look_and_say('41111', 5)) == ['11222112', '3114', '111221']

RE_TEN = re.compile('(.)\1{9}')

@given(st.text(alphabet='123456789'))
def test_day_two_splitting_theorem(text):
    assume(RE_TEN.search(text) is None)
    assert naive_deep_look_and_say(text, 5) == ''.join(deep_look_and_say(text, 5))

AOC_INPUT = '1113122113'

if __name__ == '__main__':

    def part_1(data: str):
        return len(naive_deep_look_and_say(data, 40))
        # return sum(map(len, deep_look_and_say(data, 40)))
        # return fast_length(data, 40)

    def part_2(data: str):
        return len(naive_deep_look_and_say(data, 50))
        # return sum(map(len, deep_look_and_say(data, 50)))
        # return fast_length(data, 50)

    from libaoc import simple_main, static_input
    simple_main(2015, 10, static_input(AOC_INPUT), part_1, part_2)
