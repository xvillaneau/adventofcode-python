
def reverse_engineer(key1: int, key2: int) -> int:
    first_key, value, loops = None, 1, 0
    keys = {key1, key2}
    divider = 20201227

    while True:
        value = (value * 7) % divider
        loops += 1

        if value not in keys:
            continue
        if first_key is None:
            first_key = value
            keys.discard(value)
        else:
            break

    value = 1
    for _ in range(loops):
        value = (value * first_key) % divider
    return value


def main(data: str):
    key1, key2 = (int(n) for n in data.splitlines())
    yield reverse_engineer(key1, key2)
