
from itertools import islice
import re
from typing import List, Tuple
from libaoc import files, simple_main

RE_ADDR = re.compile(r'([a-z]+)(?:\[([a-z]+)\])?')


def line_groups(line):
    groups: List[Tuple[str, str]] = RE_ADDR.findall(line)
    return [a for a, _ in groups], [b for _, b in groups if b]


def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def abba_match(word: str):
    def _abba(a, b, c, d):
        return a != b and a == d and b == c
    return any(_abba(*chrs) for chrs in window(word, 4))


def aba_matches(word: str):
    def _aba(a, b, c):
        return a != b and a == c
    return {''.join(chrs) for chrs in window(word, 3) if _aba(*chrs)}


def has_tls(line):
    net_seq, hyper_seq = line_groups(line)
    if any(abba_match(w) for w in hyper_seq):
        return False
    return any(abba_match(w) for w in net_seq)


def has_ssl(line):
    net_seq, hyper_seq = line_groups(line)
    all_aba = set([]).union(*(aba_matches(w) for w in net_seq))
    if not all_aba:
        return False

    all_bab = {b + a + b for a, b, _ in all_aba}
    return any(bab in h for bab in all_bab for h in hyper_seq)


def count_tls(lines):
    return sum(map(has_tls, lines))


def count_ssl(lines):
    return sum(map(has_ssl, lines))


if __name__ == '__main__':
    simple_main(2016, 7, files.read_lines, count_tls, count_ssl)
