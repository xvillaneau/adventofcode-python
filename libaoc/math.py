from functools import lru_cache
from itertools import count, tee
from typing import Tuple


def primes():
    lookbehind_iter = ()

    def main_iter():
        primes_explored = []
        current_prime = 3
        base_iter = count(5, 2)
        while True:
            val = next(base_iter)
            p2 = current_prime * current_prime
            while val < p2:
                if all(val % p for p in primes_explored):
                    yield val
                val = next(base_iter)
            primes_explored.append(current_prime)
            current_prime = next(lookbehind_iter)

    lookbehind_iter, primes_iter = tee(main_iter())
    yield 2
    yield 3
    yield from primes_iter


def _cached_primes():
    cache = []
    primes_iter = primes()

    def cached_iter():
        i = 0
        while True:
            if i == len(cache):
                cache.append(next(primes_iter))
            yield cache[i]
            i += 1

    return cached_iter

cached_primes = _cached_primes()

@lru_cache(maxsize=None)
def prime_factors(n):
    res = []
    ps = cached_primes()
    p = next(ps)
    while n > 1:
        m, r = divmod(n, p)
        if r:
            p = next(ps)
        else:
            res.append(p)
            n = m
    return res

@lru_cache(maxsize=None)
def all_factors(n):
    if n == 1:
        return {1}
    res = {1, n}
    for p in prime_factors(n):
        res.add(p)
        res |= all_factors(n // p)
    return res

@lru_cache()
def _gcd(a: int, b: int):
    if a == 0:
        return b
    while b != 0:
        a, b = b, a % b
    return a

def gcd(a: int, b: int):
    return _gcd(abs(a), abs(b))


def lcm(a: int, b: int):
    return a * b // gcd(a, b)


def merge_pulses(*pulses):
    if len(pulses) == 1:
        return pulses[0]
    if len(pulses) > 2:
        pivot = len(pulses) // 2
        return merge_pulses(
            merge_pulses(*pulses[:pivot]), merge_pulses(*pulses[pivot:])
        )

    (a_start, a_period), (b_start, b_period) = pulses
    x, y, g = extended_euclidian_algorithm(a_period, b_period)
    if (a_start - b_start) % g:
        raise ValueError("Sequences cannot ever match")
    period = a_period * b_period // g  # Also their Least Common Multiple
    q = (b_start - a_start) // g

    start_a = a_start + q * x * a_period
    start_b = b_start - q * y * b_period
    assert start_a % period == start_b % period
    return start_a % period, period


def extended_euclidian_algorithm(a: int, b: int) -> Tuple[int, int, int]:
    """
    Computes the integers x and y such that:
        x * a + y * b == gcd(a, b)

    Returns a tuple with x, y, and gcd(a, b)
    """
    q, r, s, t = [], [a, b], [1, 0], [0, 1]
    while r[-1] != 0:
        q.append(r[-2] // r[-1])
        r.append(r[-2] % r[-1])
        s.append(s[-2] - q[-1] * s[-1])
        t.append(t[-2] - q[-1] * t[-1])
    return s[-2], t[-2], r[-2]
