import re

RE_TAG = re.compile(r"([A-Zx\d)]*)\((\d+)x(\d+)\)")


def decompress_step(buffer: str):
    search = RE_TAG.search(buffer)
    if not search:
        return buffer, ""
    pre_tag, length, times = search.groups()
    next_buffer = buffer[search.end() :]
    decompressed = next_buffer[: int(length)] * int(times)
    return pre_tag + decompressed, next_buffer[int(length) :]


def decompressed_length(buffer):
    buffer = buffer.strip()
    out = 0
    while buffer:
        step, buffer = decompress_step(buffer)
        out += len(step)
    return out


def decompressed_length_v2(buffer):
    buffer = buffer.strip()
    out_len = 0
    while buffer:
        search = RE_TAG.search(buffer)
        if not search:
            out_len += len(buffer)
            break
        pre_tag, s_length, s_times = search.groups()
        length, times = int(s_length), int(s_times)
        buffer = buffer[search.end() :]
        out_len += len(pre_tag)
        if len(buffer) < length:
            raise ValueError(f"Recursive ain't working :/")
        out_len += times * decompressed_length_v2(buffer[:length])
        buffer = buffer[length:]

    return out_len


def main(data: str):
    yield decompressed_length(data)
    yield decompressed_length_v2(data)
