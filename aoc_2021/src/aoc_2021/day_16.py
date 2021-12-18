import math
import operator
from dataclasses import dataclass


@dataclass
class Header:
    version: int
    type_id: int
    length_type: int = 0
    length: int = 0


@dataclass
class Packet:
    value: int
    version: int
    size: int


class BitSequence:
    def __init__(self, data: str):
        self.data = bytes.fromhex(data)
        self._bit_pt = 8
        self._bytes_pt = 0

    def take(self, bits: int) -> int:
        if bits <= 0:
            return 0
        if self._bytes_pt >= len(self.data):
            raise StopIteration

        byte = self.data[self._bytes_pt]
        take = min(bits, self._bit_pt)
        mask = (1 << self._bit_pt) - 1
        value = (byte & mask) >> (self._bit_pt - take)

        self._bit_pt -= take
        if self._bit_pt == 0:
            self._bit_pt = 8
            self._bytes_pt += 1
        rem = bits - take
        return (value << rem) + self.take(rem)


def _read_literal(bits: BitSequence) -> tuple[int, int]:
    value, size, flag = 0, 0, True
    while flag:
        chunk = bits.take(5)
        value = (value << 4) + (chunk & 0x0f)
        size += 5
        flag = bool(chunk & 0x10)
    return value, size


OPERATORS = [
    sum,
    math.prod,
    min,
    max,
    None,  # Literal
    operator.gt,
    operator.lt,
    operator.eq,
]


def compute_packets(bits: BitSequence) -> Packet:
    """
    returns: value of packet, sum of versions, total size in bits
    """

    # Read header
    version = bits.take(3)
    type_id = bits.take(3)

    if type_id == 4:  # Literal
        value, size = _read_literal(bits)
        print("Literal value:", value)
        return Packet(value, version, size + 6)

    if bits.take(1) == 0:
        payload_size = bits.take(15)
        head_size = 22
        children = []
        while payload_size > 0:
            children.append(compute_packets(bits))
            payload_size -= children[-1].size
    else:
        n_children = bits.take(11)
        head_size = 18
        children = [compute_packets(bits) for _ in range(n_children)]

    values = [c.value for c in children]
    assert 0 <= type_id < 8 and type_id != 4
    if type_id <= 3:
        value = int(OPERATORS[type_id](values))
    else:
        assert len(values) == 2
        value = int(OPERATORS[type_id](*values))

    sum_version = version + sum(c.version for c in children)
    sum_size = head_size + sum(c.size for c in children)
    print("Running", OPERATORS[type_id], "on", values)
    return Packet(value, sum_version, sum_size)


def main(data: str):
    packet = compute_packets(BitSequence(data.strip()))
    yield packet.version
    yield packet.value
