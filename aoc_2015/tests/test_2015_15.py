from aoc_2015.day_15 import best_recipes

example = [
    "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
    "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3",
]

def test_2015_day_15():
    assert best_recipes(example) == (62842880, 57600000)
