import json

def sum_decode(strings):
    return sum(len(s) - len(eval(s)) for s in strings)

def sum_encode(strings):
    return sum(len(json.dumps(s)) - len(s) for s in strings)

def test_sums():
    strings = ['""', '"abc"', r'"aaa\"aaa"', r'"\x27"']
    assert sum_decode(strings) == 12
    assert sum_encode(strings) == 19

def main(data: str):
    lines = data.splitlines()
    yield sum_decode(lines)
    yield sum_encode(lines)
