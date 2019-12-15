import re
import numpy as np

def iter_quantities(n_ingredients: int, total=100):
    if n_ingredients == 1:
        yield (total,)
        return
    if total == 0:
        yield (0,) * n_ingredients
        return
    for qty in range(total + 1):
        others = iter_quantities(n_ingredients - 1, total - qty)
        for other in others:
            yield (qty,) + other


def calc_score(quantities: np.ndarray, properties):
    totals = (
        quantities[:, np.newaxis]
        .repeat(4, axis=1)
        .__mul__(properties)
        .sum(axis=0)
    )
    return np.maximum(totals, np.zeros(totals.size, np.int)).prod()

RE_PROP = re.compile(
    r"(?:\w+): capacity (-?\d+), durability (-?\d+), "
    r"flavor (-?\d+), texture (-?\d+), calories (-?\d+)"
)

def parse_properties(properties):
    for line in properties:
        yield map(int, RE_PROP.match(line).groups())

def best_recipes(ingredients_list, cal_lim=500):
    properties = np.array([
        [cap, dur, fla, tex, cal]
        for cap, dur, fla, tex, cal
        in parse_properties(ingredients_list)
    ])
    calories = properties[:, 4]
    properties = properties[:, :4]
    max_all, max_cal = 0, 0
    for qties in iter_quantities(len(ingredients_list)):
        qties = np.array(qties)
        score = calc_score(qties, properties)
        if score > max_all:
            max_all = score
        if score > max_cal and np.sum(qties * calories) == cal_lim:
            max_cal = score
    return max_all, max_cal

if __name__ == '__main__':
    from libaoc import tuple_main, files
    tuple_main(2015, 15, files.read_lines, best_recipes)
