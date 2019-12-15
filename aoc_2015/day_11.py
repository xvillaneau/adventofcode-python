from string import ascii_lowercase

_a, _z, _banned = ord('a'), ord('z'), set(b'iol')

class PasswordGen:

    def __init__(self, password: bytes):
        assert all(chr(c) in ascii_lowercase for c in password)
        self._pw = bytearray(password)
        self._pre_sanitize()

    def _pre_sanitize(self):
        for i, c in enumerate(self._pw):
            if c in _banned:
                break
        else:
            return
        self._pw[i+1:] = b'z' * (len(self._pw) - i - 1)

    def __iter__(self):
        return self

    def __next__(self):
        i = len(self._pw) - 1
        while i >= 0:
            new = self._pw[i] + 1
            if new > _z:
                self._pw[i] = _a
                i -= 1
                continue
            if new in _banned:
                new += 1
            self._pw[i] = new
            break
        return bytes(self._pw)

def _has_two_pairs(pw: bytes):
    if not pw:
        return False
    a, *s = pw
    pairs = set()
    for b in s:
        if a == b:
            pairs.add(a)
            if len(pairs) >= 2:
                return True
        a = b
    return False

def _has_triplet(pw: bytes):
    a, b, *s = pw
    for c in s:
        if c == b + 1 == a + 2:
            return True
        a, b = b, c
    return False

def is_valid(pw: bytes):
    return _has_triplet(pw) and _has_two_pairs(pw)

def next_valid(password: str):
    return next(
        pw for pw in PasswordGen(password.encode()) if is_valid(pw)
    ).decode()

def two_next_valid(password: str):
    first = next_valid(password)
    second = next_valid(first)
    return first, second

if __name__ == '__main__':
    from libaoc import static, tuple_main
    tuple_main(2015, 11, static('cqjxjnds'), two_next_valid)
