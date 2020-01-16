from collections import deque

def not_white_elephant(n: int):
    elves = deque(range(1, n + 1))
    while len(elves) > 1:
        elves.rotate(-1)
        elves.popleft()
    return elves[0]

def still_not_white_elephant(n: int):
    elves = deque(range(1, n + 1))
    elves.rotate(-(len(elves) // 2))
    if len(elves) % 2:
        elves.popleft()
        elves.rotate(-1)
    while len(elves) > 1:
        elves.popleft()
        if len(elves) == 1:
            break
        elves.popleft()
        elves.rotate(-1)
    return elves[0]

def main(data: str):
    num = int(data)
    yield not_white_elephant(num)
    yield still_not_white_elephant(num)
