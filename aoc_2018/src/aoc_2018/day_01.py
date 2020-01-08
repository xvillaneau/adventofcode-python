from itertools import accumulate, cycle


def main(data):
    deltas = [int(line) for line in data.splitlines()]

    yield sum(deltas)

    visited = {0}
    for freq in accumulate(cycle(deltas)):
        if freq in visited:
            yield freq
            return
        visited.add(freq)
