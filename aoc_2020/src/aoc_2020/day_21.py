from functools import reduce
from operator import and_, or_
import re

Data = list[tuple[set[str], set[str]]]


def parse_data(data: list[str]):
    out = []
    for line in data:
        ingredients, allergens = re.match(
            r'(.*)\(contains (.*)\)', line
        ).groups()
        out.append((set(ingredients.split()), set(allergens.split(', '))))
    return out


def match_allergens(data: Data):
    all_ingredients = reduce(or_, (i for i, _ in data), set())
    all_allergens = reduce(or_, (a for _, a in data), set())

    candidates: dict[str, set[str]] = {}
    for allergen in all_allergens:
        ing = (i for i, a in data if allergen in a)
        candidates[allergen] = reduce(and_, ing, all_ingredients)

    allergens: dict[str, str] = {}
    allocated: set[str] = set()
    while candidates:
        for allergen, ingredients in candidates.items():
            ingredients -= allocated
            if len(ingredients) == 1:
                break
            if len(ingredients) == 0:
                raise ValueError(f"Failed to solve for {allergen}")
        else:
            raise ValueError("Cannot solve")

        ingredient, = candidates.pop(allergen)
        allocated.add(ingredient)
        allergens[allergen] = ingredient

    return allergens


def count_safe_ingredients(data: Data, allergens: dict[str, str]):
    all_allergens = set(allergens.values())
    return sum(
        len(ingredients - all_allergens)
        for ingredients, _ in data
    )


def make_canonical(allergens: dict[str, str]):
    keys = sorted(allergens.keys())
    return ','.join(allergens[k] for k in keys)


def main(data: str):
    data = parse_data(data.splitlines())
    allergens = match_allergens(data)
    yield count_safe_ingredients(data, allergens)
    yield make_canonical(allergens)
