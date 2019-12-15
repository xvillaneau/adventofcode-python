
import json

def sum_decode(strings):
    return sum(len(s) - len(eval(s)) for s in strings)

def sum_encode(strings):
    return sum(len(json.dumps(s)) - len(s) for s in strings)

def test_sums():
    strings = ['""', '"abc"', r'"aaa\"aaa"', r'"\x27"']
    assert sum_decode(strings) == 12
    assert sum_encode(strings) == 19

if __name__ == '__main__':
    from libaoc import simple_main, files
    simple_main(2015, 8, files.read_lines, sum_decode, sum_encode)
