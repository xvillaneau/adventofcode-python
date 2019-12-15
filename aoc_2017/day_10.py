from typing import List, Tuple

Loop = List[int]


def twist(loop: Loop, length: int) -> Loop:
    assert len(loop) >= length
    return loop[:length][::-1] + loop[length:]


def move(loop: Loop, step: int) -> Loop:
    base_step = step % len(loop)
    return loop[base_step:] + loop[:base_step]


def twist_round(lengths: List[int], loop: Loop, skip, pos) -> Tuple[Loop, int, int]:

    mod_loop = move(loop, pos)
    moves_sum = pos

    for length in lengths:
        mod_loop = move(twist(mod_loop, length), skip + length)
        moves_sum += skip + length
        skip += 1

    return move(mod_loop, -moves_sum), skip, moves_sum % len(loop)


def str_to_lengths(str_input: str):
    padding = [17, 31, 73, 47, 23]
    return [ord(c) for c in str_input] + padding


def sparse_hash(lengths: List[int]) -> Loop:
    loop = list(range(256))
    skip, pos = 0, 0
    for _ in range(64):
        loop, skip, pos = twist_round(lengths, loop, skip, pos)
    return loop


def reduce_block(block: List[int]):
    out = block[0]
    for i in block[1:]:
        out = out ^ i
    return out


def dense_hash(long_hash):
    assert len(long_hash) == 256
    return [reduce_block(long_hash[i:i+16]) for i in range(0, 256, 16)]


def hex_hash(short_hash: List[int]):
    return ''.join(f'{i:02X}' for i in short_hash).lower()


def int_hash(str_in: str) -> int:
    hash_bytes = dense_hash(sparse_hash(str_to_lengths(str_in)))
    return sum(b * 256 ** i for i, b in enumerate(hash_bytes[::-1]))


def full_hash(str_in: str):
    return hex_hash(dense_hash(sparse_hash(str_to_lengths(str_in))))


def day_10(data: str):
    instructions = [int(i) for i in data.split(',')]
    hashed, _, _ = twist_round(instructions, list(range(256)), 0, 0)
    yield hashed[0] * hashed[1]
    yield full_hash(data)

if __name__ == '__main__':
    from libaoc import iter_main, files
    iter_main(2017, 10, files.read_full, day_10)
