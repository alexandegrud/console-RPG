from base.models import Weapon, Armor, Player, Enemy
from base.autobattle import autobattle

def test_autobattle_player_wins():
    # Player stronger and always hits
    pw = Weapon(name="PW", damage=5, hit_chance=100)
    pa = Armor(name="PA", defense=0)
    ew = Weapon(name="EW", damage=1, hit_chance=0)
    ea = Armor(name="EA", defense=0)
    player = Player(name="Hero", life=10, weapon=pw, armor=pa)
    enemy = Enemy(name="Foe", life=3, weapon=ew, armor=ea)
    logs = []
    won = autobattle(player, enemy, output_func=logs.append)
    assert won is True
    assert enemy.life == 0

def test_autobattle_enemy_wins():
    pw = Weapon(name="PW", damage=1, hit_chance=0)
    pa = Armor(name="PA", defense=0)
    ew = Weapon(name="EW", damage=5, hit_chance=100)
    ea = Armor(name="EA", defense=0)
    player = Player(name="Hero", life=3, weapon=pw, armor=pa)
    enemy = Enemy(name="Foe", life=10, weapon=ew, armor=ea)
    logs = []
    won = autobattle(player, enemy, output_func=logs.append)
    assert won is False
    assert player.life == 0
