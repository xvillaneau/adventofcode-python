from collections import deque, defaultdict
from hashlib import md5
import re
from typing import List, Dict, Deque, Tuple

POOL_SIZE = 10
RE_HASH = re.compile(r"((.)\2\2+)")


def run_hash(seed: bytes, index: int, queue: deque):
    hex_hash: str = md5(seed + str(index).encode()).hexdigest()
    has_three = False
    for group, char in RE_HASH.findall(hex_hash):
        size = len(group)
        if not has_three and size == 3:
            queue.append((index, 3, char))
        elif size == 5:
            queue.append((index, 5, char))


def find_hashes(seed: bytes, n=64, stretches=0, debug=False):
    index = 0
    valid_indices: List[int] = []
    pending: Deque[Tuple[int, str]] = deque()
    quintuples: Dict[str, int] = defaultdict(int)

    while len(valid_indices) < n:

        # Remove pending hashes that didn't make it
        while pending:
            ind, char = pending[0]
            if ind + 1000 >= index:
                break
            if debug:
                print("Didn't make it:", (ind, char))
            pending.popleft()

        # Compute the hash
        hex_hash: str = md5(seed + str(index).encode()).hexdigest()
        for _ in range(stretches):
            hex_hash = md5(hex_hash.encode()).hexdigest()

        # Process the patterns in said hash
        first = True
        for group, char in RE_HASH.findall(hex_hash):
            if first:
                if debug:
                    print("New candidate:", (index, char))
                pending.append((index, char))
                first = False
            if len(group) >= 5:
                if debug:
                    print("Found quintuple:", (index, char))
                quintuples[char] = index

        # Validate the pending passwords
        while pending:
            ind, char = pending[0]
            if quintuples[char] <= ind:
                break
            if debug:
                print(
                    "New valid hash:",
                    (ind, char),
                    "with quintuple at",
                    quintuples[char],
                )
            pending.popleft()
            valid_indices.append(ind)

        index += 1

    return valid_indices[n - 1]


def main(data: str):
    seed = data.encode()
    yield find_hashes(seed)
    yield find_hashes(seed, stretches=2016)
