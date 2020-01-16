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

if __name__ == '__main__':
    from libaoc import static_input, simple_main
    simple_main(
        2015, 19, static_input(3001330), not_white_elephant, still_not_white_elephant
    )
