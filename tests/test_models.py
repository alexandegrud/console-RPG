from base.models import Weapon, Armor, Player, Enemy

def test_entity_damage_and_death():
    w = Weapon(name="W", damage=5, hit_chance=100)
    a = Armor(name="A", defense=2)
    attacker = Player(name="Att", life=10, weapon=w, armor=a)
    defender = Enemy(name="Def", life=6, weapon=w, armor=a)
    assert attacker.attack_hit()  # hit_chance 100 -> should be True
    dmg = attacker.compute_damage()
    assert dmg == 3
    defender.receive_damage(dmg)
    assert defender.life == 3
    defender.receive_damage(5)
    assert defender.life == 0
    assert not defender.is_alive
