
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

def main(_):
    # TODO: Read data from file
    yield get_code(index_of(2978, 3083))
