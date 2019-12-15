from itertools import islice
from aoc_2015.day_11 import PasswordGen, is_valid, next_valid

def test_incr():
    pw = PasswordGen(b'xx')
    assert tuple(islice(pw, 4)) == (b'xy', b'xz', b'ya', b'yb')

def test_incr_overflow():
    pw = PasswordGen(b'zzzzzz')
    assert next(pw) == b'aaaaaa'

def test_incr_banned():
    assert next(PasswordGen(b'an')) == b'ap'
    assert next(PasswordGen(b'hzz')) == b'jaa'

def test_valid():
    assert not is_valid(b'abbceffg')
    assert not is_valid(b'abbcegjk')
    assert is_valid(b'abcdffaa')
    assert is_valid(b'ghjaabcc')

def test_next_valid():
    assert next_valid('abcdefgh') == 'abcdffaa'
    assert next_valid('ghijklmn') == 'ghjaabcc'
