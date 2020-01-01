from aoc_2015.day_17 import count_container_combinations

def test_containers():
    containers = [20, 15, 10, 5, 5]
    assert count_container_combinations(containers, 25) == (4, 3)
