from itertools import count
from hashlib import md5
from multiprocessing import Pool

SIZE = 10000


def code_hash_batch(params):
    key, limit, batch_start, batch_size = params
    base = md5(key)
    for i in range(batch_start, batch_start + batch_size):
        full_hash = base.copy()
        full_hash.update(str(i).encode())
        head = int.from_bytes(full_hash.digest()[:3], "big")
        if head <= limit:
            return i
    return -1


def find_hash_pool(key, lim):
    with Pool() as pool:
        params = ((key, lim, start, SIZE) for start in count(1, SIZE))
        results = pool.imap(code_hash_batch, params)
        return next(i for i in results if i >= 0)


def main(data: str):
    key = data.encode()
    yield find_hash_pool(key, 15)
    yield find_hash_pool(key, 0)
