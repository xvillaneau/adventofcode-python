from itertools import count
from hashlib import md5

def code_hash(key: bytes, number: int) -> bytes:
    hash_input = key + str(number).encode()
    return md5(hash_input).digest()

def is_valid_hash_5(digest: bytes):
    return int.from_bytes(digest[:3], 'big') < 16

def is_valid_hash_6(digest: bytes):
    return int.from_bytes(digest[:3], 'big') == 0

def coin_mine_5(key: bytes):
    return next(i for i in count(1) if is_valid_hash_5(code_hash(key, i)))

def coin_mine_6(key: bytes):
    return next(i for i in count(1) if is_valid_hash_6(code_hash(key, i)))

def test_mine():
    assert coin_mine_5(b'abcdef') == 609043

def main(data: str):
    yield coin_mine_5(data.encode())
    yield coin_mine_6(data.encode())
