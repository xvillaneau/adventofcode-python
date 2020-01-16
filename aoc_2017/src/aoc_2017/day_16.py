import re
from functools import partial, lru_cache
from typing import Callable, Generator, List

RE_SPIN = re.compile(r"^s(\d+)$")
RE_XCHG = re.compile(r"^x(\d+)/(\d+)$")
RE_PART = re.compile(r"^p([a-z]+)/([a-z]+)$")

Op = Callable[[List[int]], List[int]]


def spin(x: int, vect: List[int]):
    return vect[-x:] + vect[:-x]


def exchange(a: int, b: int, vect: List[int]):
    out = vect.copy()
    out[a] = vect[b]
    out[b] = vect[a]
    return out


def partner(a: int, b: int, vect: List[int]):
    ia, ib = vect.index(a), vect.index(b)
    return exchange(ia, ib, vect)


def extract_instructions(file_str: str) -> Generator[Op, None, None]:

    for instruction in file_str.split(','):

        m_spin = RE_SPIN.match(instruction)
        m_xchg = RE_XCHG.match(instruction)
        m_part = RE_PART.match(instruction)

        if m_spin is not None:
            x = int(m_spin.groups()[0])
            yield partial(spin, x)

        elif m_xchg is not None:
            a, b = int(m_xchg.groups()[0]), int(m_xchg.groups()[1])
            yield partial(exchange, a, b)

        elif m_part is not None:
            a, b = ord(m_part.groups()[0]), ord(m_part.groups()[1])
            yield partial(partner, a, b)

        else:
            raise ValueError


def dance_func(instructions: str):
    operations = list(extract_instructions(instructions))

    @lru_cache(maxsize=None)
    def _dance(programs: str) -> str:
        prog_ints = [ord(c) for c in programs]
        for op in operations:
            prog_ints = op(prog_ints)
        return ''.join(chr(c) for c in prog_ints)

    return _dance

P_16 = "abcdefghijklmnop"

def dance(instructions: str, programs: str = P_16) -> str:
    return dance_func(instructions)(programs)


def billion_dances(instructions: str, programs: str = P_16, n=1_000_000_000):
    _dance = dance_func(instructions)
    progs_ini = programs
    for i in range(n):
        programs = _dance(programs)
        if programs == progs_ini:
            return billion_dances(instructions, programs, n=(n % (i+1)))
    return programs


def main(data: str):
    yield dance(data)
    yield billion_dances(data)
