from aoc_2020.day_21 import *

EXAMPLE = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""".strip().splitlines()


def test_parse_data():
    assert parse_data(EXAMPLE) == [
        ({"mxmxvkd", "kfcds", "sqjhc", "nhms"}, {"dairy", "fish"}),
        ({"trh", "fvjkl", "sbzzf", "mxmxvkd"}, {"dairy"}),
        ({"sqjhc", "fvjkl"}, {"soy"}),
        ({"sqjhc", "mxmxvkd", "sbzzf"}, {"fish"}),
    ]


def test_match_allergens():
    data = parse_data(EXAMPLE)
    assert match_allergens(data) == {
        "dairy": "mxmxvkd", "fish": "sqjhc", "soy": "fvjkl"
    }


def test_count_safe_ingredients():
    data = parse_data(EXAMPLE)
    assert count_safe_ingredients(data, match_allergens(data)) == 5


def test_make_canonical():
    data = parse_data(EXAMPLE)
    assert make_canonical(match_allergens(data)) == "mxmxvkd,sqjhc,fvjkl"
