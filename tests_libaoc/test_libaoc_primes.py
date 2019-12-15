from libaoc.primes import merge_pulses

def test_merge_pulses():
    assert merge_pulses((0, 3), (0, 5)) == (0, 15)
    assert merge_pulses((1, 3), (0, 5)) == (10, 15)
    assert merge_pulses((2, 3), (0, 5)) == (5, 15)
    assert merge_pulses((12, 246), (60, 207)) == (12066, 16974)
