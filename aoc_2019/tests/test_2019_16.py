from aoc_2019.day_16 import fft, full_signal


def test_fft():
    assert fft("12345678", 4) == "01029498"
    assert fft("80871224585914546619083218645595") == "24176176"
    assert fft("19617804207202209144916044189917") == "73745418"
    assert fft("69317163492948606335995924319873") == "52432133"


def test_full_signal():
    assert full_signal("03036732577212944063491565474664") == "84462026"
    assert full_signal("02935109699940807407585447034323") == "78725270"
    assert full_signal("03081770884921959731165446850517") == "53553731"
