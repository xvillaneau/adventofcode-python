
from libaoc import simple_main, files


def changes(lines):
    return sum(map(int, lines))


def visited_twice(lines):
    deltas = list(map(int, lines))
    visited, freq = {0}, 0

    while True:
        for delta in deltas:
            freq += delta
            if freq in visited:
                return freq
            visited.add(freq)


if __name__ == '__main__':
    simple_main(2018, 1, files.read_lines, changes, visited_twice)
