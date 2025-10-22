from dataclasses import dataclass
import random

@dataclass
class Weapon:
    name: str
    damage: int
    hit_chance: int
    description: str = ""

@dataclass
class Armor:
    name: str
    defense: int
    description: str = ""

class Entity:
    def __init__(self, name: str, life: int, weapon: Weapon, armor: Armor, description: str = ""):
        self.name = name
        self.max_life = life
        self.life = life
        self.weapon = weapon
        self.armor = armor
        self.description = description

    @property
    def is_alive(self) -> bool:
        return self.life > 0

    def receive_damage(self, dmg: int):
        self.life = max(0, self.life - dmg)

    def attack_hit(self) -> bool:
        chance = random.randint(0, 100)
        return self.weapon.hit_chance >= chance

    def compute_damage(self) -> int:
        raw = self.weapon.damage
        if raw > self.armor.defense:
            return raw - self.armor.defense
        return 0

class Player(Entity):
    pass

class Enemy(Entity):
    pass

class Room:
    def __init__(self, idx: int, description: str, enemy: Enemy | None = None):
        self.idx = idx
        self.description = description
        self.enemy = enemy

    @property
    def is_empty(self):
        return self.enemy is None or not self.enemy.is_alive

class Dungeon:
    def __init__(self, rooms: list[Room], start_index: int = 0):
        self.rooms = rooms
        self.start_index = start_index
        self.exit_index = len(rooms) - 1
