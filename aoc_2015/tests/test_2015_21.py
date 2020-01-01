from aoc_2015.day_21 import Character, player_wins

def test_combat():
    player = Character(8, 5, 5)
    boss = Character(12, 7, 2)
    assert player_wins(player, boss)
    assert player.hit_points == 2
