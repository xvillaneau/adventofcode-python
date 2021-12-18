import pytest

from aoc_2021.day_16 import BitSequence, compute_packets


EXAMPLE_VERSIONS = [  # Hex string, value, version
    ("D2FE28", 6),
    ("38006F45291200", 9),
    ("EE00D40C823060", 14),
    ("8A004A801A8002F478", 16),
    ("620080001611562C8802118E34", 12),
    ("C0015000016115A2E0802F182340", 23),
    ("A0016C880162017C3686B18A3D4780", 31),
]
EXAMPLE_VALUES = [  # Hex string, value, version
    ("D2FE28", 2021),
    ("38006F45291200", 1),
    ("EE00D40C823060", 3),
    ("C200B40A82", 3),
    ("04005AC33890", 54),
    ("880086C3E88112", 7),
    ("CE00C43D881120", 9),
    ("D8005AC2A8F0", 1),
    ("F600BC2D8F", 0),
    ("9C005AC2F8F0", 0),
    ("9C0141080250320F1802104A08", 1),
]


@pytest.mark.parametrize("data,version", EXAMPLE_VERSIONS)
def test_version_sums(data, version):
    packet = compute_packets(BitSequence(data))
    assert packet.version == version


@pytest.mark.parametrize("data,value", EXAMPLE_VALUES)
def test_values(data, value):
    packet = compute_packets(BitSequence(data))
    assert packet.value == value
