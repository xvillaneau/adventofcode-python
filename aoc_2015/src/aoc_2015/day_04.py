from itertools import count
from hashlib import md5


def code_hash(base, number: int) -> int:
    full_hash = base.copy()
    full_hash.update(str(number).encode())
    return int.from_bytes(full_hash.digest()[:3], "big")


def coin_mine_5(base):
    return next(i for i in count(1) if code_hash(base, i) < 16)


def coin_mine_6(base):
    return next(i for i in count(1) if code_hash(base, i) == 0)


def test_mine():
    assert coin_mine_5(md5(b'abcdef')) == 609043


def main(data: str):
    base = md5(data.encode())
    yield coin_mine_5(base)
    yield coin_mine_6(base)
