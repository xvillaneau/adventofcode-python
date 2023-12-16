def main(data: str):
    elves = sorted(
        sum(map(int, elf.splitlines()))
        for elf in data.split("\n\n")
    )
    yield elves[-1]
    yield sum(elves[-3:])
