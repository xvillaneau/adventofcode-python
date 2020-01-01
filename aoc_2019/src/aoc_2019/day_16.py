import numpy as np

PATTERN = np.array([0, 1, 0, -1])


def build_pattern(index: int, length: int):
    base_pattern = np.repeat(PATTERN, index + 1)
    repeats = 1 + length // (4 + 4 * index)
    return np.tile(base_pattern, repeats)[1 : length + 1]


def build_patterns(length: int, n_patterns=0):
    return np.array([build_pattern(i, length) for i in range(n_patterns or length)])


def fft(signal: str, n_phases=100):
    signal = np.array([int(i) for i in signal])
    patterns = build_patterns(len(signal))
    for _ in range(n_phases):
        signal = np.abs(patterns @ signal) % 10
    return "".join(map(str, signal[:8]))


def full_signal(signal: str):
    offset = int(signal[:7])
    signal = np.array([int(i) for i in signal])
    assert offset >= len(signal) * 5_000
    n, r = divmod(len(signal) * 10_000 - offset, len(signal))
    signal = np.concatenate((signal[-r:], np.tile(signal, n)))[::-1]
    for _ in range(100):
        signal = np.add.accumulate(signal) % 10
    return "".join(map(str, signal[:-9:-1]))


def main(data: str):
    yield fft(data)
    yield full_signal(data)
