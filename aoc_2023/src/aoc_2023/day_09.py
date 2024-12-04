
def extrapolate(values: list[int]) -> tuple[int, int]:
    a = values[0]
    deltas = []
    for b in values[1:]:
        deltas.append(b - a)
        a = b
    if any(deltas):
        d0, dn = extrapolate(deltas)
        return values[0] - d0, values[-1] + dn
    return a, a


def main(data: str):
    sequences = (
        [int(n) for n in line.split()]
        for line in data.splitlines()
    )
    results = [extrapolate(seq) for seq in sequences]
    yield sum(b for _, b in results)
    yield sum(a for a, _ in results)
