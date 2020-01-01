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

if __name__ == '__main__':
    from libaoc import simple_main
    day_input = b'yzbqklnj'
    reader = lambda year, day: day_input
    simple_main(2015, 4, reader, coin_mine_5, coin_mine_6)
