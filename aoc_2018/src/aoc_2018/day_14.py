
from typing import List

def digits(n):
    if n == 0:
        return [0]
    out = []
    while n > 0:
        n, digit = divmod(n, 10)
        out.append(digit)
    out.reverse()
    return out


def un_digits(ns: List[int]):
    out = 0
    factor = 1
    for n in reversed(ns):
        out += n * factor
        factor *= 10
    return out


class StatePart1:

    def __init__(self):
        self.recipes = [3, 7]
        self.elf_1 = 0
        self.elf_2 = 1

    def step(self):
        val_1, val_2 = self.recipes[self.elf_1], self.recipes[self.elf_2]
        self.recipes.extend(digits(val_1 + val_2))

        n_recipes = len(self.recipes)
        self.elf_1 += 1 + val_1
        self.elf_2 += 1 + val_2
        self.elf_1 %= n_recipes
        self.elf_2 %= n_recipes

    def step_til(self, offset):
        while len(self.recipes) < offset + 10:
            self.step()
        return un_digits(self.recipes[offset:offset + 10])

    def __str__(self):
        res = []
        for i, n in enumerate(self.recipes):
            if i == self.elf_1:
                res.append(f'({n})')
            elif i == self.elf_2:
                res.append(f'[{n}]')
            else:
                res.append(f' {n} ')
        return ''.join(res)


class StatePart2:

    def __init__(self, target: List[int]):
        self.recipes = [3, 7]
        self.elf_1 = 0
        self.elf_2 = 1
        self.target = target
        self._len_target = len(target)
        self.found = -1

    def step(self):
        val_1, val_2 = self.recipes[self.elf_1], self.recipes[self.elf_2]
        for d in digits(val_1 + val_2):
            self.recipes.append(d)
            if self.recipes[-self._len_target:] == self.target:
                self.found = len(self.recipes) - self._len_target

        n_recipes = len(self.recipes)
        self.elf_1 += 1 + val_1
        self.elf_2 += 1 + val_2
        self.elf_1 %= n_recipes
        self.elf_2 %= n_recipes

    def step_til_found(self):
        while self.found < 0:
            self.step()
        return self.found

    def __str__(self):
        res = []
        for i, n in enumerate(self.recipes):
            if i == self.elf_1:
                res.append(f'({n})')
            elif i == self.elf_2:
                res.append(f'[{n}]')
            else:
                res.append(f' {n} ')
        return ''.join(res)
