
def index_of(row: int, col: int):
    diag = row + col - 1
    base = (diag * diag - diag + 2) // 2
    return base + col - 1

_cache = [20151125]

def get_code(index: int):
    if index <= len(_cache):
        return _cache[index - 1]
    start, code = len(_cache), _cache[-1]
    for _ in range(start, index):
        code *= 252533
        code = code % 33554393
        _cache.append(code)
    return code

def part_1(coords):
    return get_code(index_of(*coords))

if __name__ == '__main__':
    from libaoc import simple_main, static_input
    puzzle_input = static_input((2978, 3083))
    simple_main(2015, 25, puzzle_input, part_1)
