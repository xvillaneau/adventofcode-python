from itertools import islice
from functools import lru_cache

def inverse(data: str):
    result = ""
    for char in reversed(data):
        result += "1" if char == "0" else "0"
    return result


def dragon_iter_v1(data: str):
    yield from data
    while True:
        for char in "0" + inverse(data):
            yield char
            data += char


def dragon_iter_v2(data: str):
    yield from data
    anti_data = inverse(data)
    zeros = dragon_iter_v2("001001100011011")
    while True:
        yield next(zeros)
        yield from anti_data
        yield next(zeros)
        yield from data


dragon_iter = dragon_iter_v2


def pairs_iter(iterator):
    try:
        while True:
            yield next(iterator), next(iterator)
    except StopIteration:
        return


def factors_of_2(n: int):
    res = 0
    while n % 2 == 0:
        res += 1
        n //= 2
    return res


CHECKSUM_PAIRS = {"01": "0", "10": "0", "11": "1", "00": "1"}


@lru_cache(maxsize=65536)
def _slice_checksum(data_slice: str):
    while len(data_slice) > 1:
        next_slice = ""
        for i in range(0, len(data_slice), 2):
            next_slice += CHECKSUM_PAIRS[data_slice[i:i+2]]
        data_slice = next_slice
    return data_slice


def compute_checksum(start_data: str, disk_size: int, slice_min=10):
    depth = factors_of_2(disk_size)
    slice_size = min(1 << slice_min, 1 << depth)
    n_slices = disk_size // slice_size
    stack_size = depth - min(slice_min, depth)
    stack, indices = [""] * stack_size, list(range(stack_size))
    checksum, data_iter = "", dragon_iter(start_data)
    for _ in range(n_slices):
        data_slice = ''.join(islice(data_iter, slice_size))
        char = _slice_checksum(data_slice)
        for i in indices:
            if not stack[i]:
                stack[i] = char
                break
            char = CHECKSUM_PAIRS[stack[i] + char]
            stack[i] = ""
        else:
            checksum += char
    return checksum


if __name__ == '__main__':
    from functools import partial
    from libaoc import simple_main, static_input
    _input = static_input("10111011111001111")
    part_1 = partial(compute_checksum, disk_size=272)
    part_2 = partial(compute_checksum, disk_size=35651584)
    simple_main(2016, 16, _input, part_1, part_2)
