from aoc_2016.day_15 import Disc, find_first_align

example = [
    "Disc #1 has 5 positions; at time=0, it is at position 4.",
    "Disc #2 has 2 positions; at time=0, it is at position 1.",
]

def test_aligned_at():
    disc_1 = Disc.from_str(example[0])
    assert not disc_1.aligned_at(0)
    assert disc_1.aligned_at(1)
    assert not disc_1.aligned_at(2)
    assert disc_1.aligned_at(6)

    disc_2 = Disc.from_str(example[1])
    assert not disc_2.aligned_at(0)
    assert disc_2.aligned_at(1)
    assert not disc_2.aligned_at(2)
    assert disc_2.aligned_at(3)


def test_find_first_align():
    assert find_first_align(example) == 5
