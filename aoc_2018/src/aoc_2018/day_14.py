def digits(n):
    if n == 0:
        return [0]
    out = []
    while n > 0:
        n, digit = divmod(n, 10)
        out.append(digit)
    return out[::-1]


def main(data: str):
    number = int(data)

    recipes = [3, 7]
    elf_1, elf_2, len_recipes = 0, 1, 2
    _digits = [digits(n) for n in range(19)]

    p1_target = number + 10
    while len_recipes < p1_target:
        val_1, val_2 = recipes[elf_1], recipes[elf_2]
        recipes.extend(_digits[(new := val_1 + val_2)])
        len_recipes += 1 + new // 10
        elf_1 = (elf_1 + val_1 + 1) % len_recipes
        elf_2 = (elf_2 + val_2 + 1) % len_recipes

    yield "".join(map(str, recipes[number:number + 10]))

    p2_target = digits(number)
    n_digits = len(p2_target)

    def done():
        return recipes[-n_digits:] == p2_target

    while 1:
        val_1, val_2 = recipes[elf_1], recipes[elf_2]
        for d in _digits[val_1 + val_2]:
            recipes.append(d)
            len_recipes += 1
            if done():
                yield len_recipes - n_digits
                return
        elf_1 = (elf_1 + val_1 + 1) % len_recipes
        elf_2 = (elf_2 + val_2 + 1) % len_recipes
