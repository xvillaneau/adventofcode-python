from itertools import accumulate

def main(data: str):
    moves = [1 if char == "(" else -1 for char in data]
    yield sum(moves)
    yield next(
        pos
        for pos, floor in enumerate(accumulate(moves), start=1)
        if floor == -1
    )
