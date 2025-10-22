import json, random
from pathlib import Path
from .models import Weapon, Armor, Player, Enemy, Room, Dungeon
from .controller import GameController, InputProvider

DATA_DIR = Path(__file__).parent.parent / "data"

def load_json(name):
    return json.loads((DATA_DIR / name).read_text(encoding='utf-8'))

def create_player():
    p = load_json("player.json")
    name = random.choice(p["names"])
    description = random.choice(p["descriptions"])
    weapon = Weapon(**p["weapon"])
    armor = Armor(**p["armor"])
    player = Player(name=name, life=p["stats"]["life"], weapon=weapon, armor=armor, description=description)
    return player

def create_enemies():
    e = load_json("enemies.json")
    enemies = []
    for item in e["enemies"]:
        weapon = Weapon(**item["weapon"])
        armor = Armor(**item["armor"])
        enemy = Enemy(name=item["name"], life=item["life"], weapon=weapon, armor=armor, description=item["description"])
        enemies.append(enemy)
    return enemies

def create_dungeon(num_rooms=5):
    rooms_data = load_json("rooms.json")
    room_texts = rooms_data
    enemies = create_enemies()
    rooms = []
    for i in range(num_rooms):
        # randomly decide if room has enemy (except start and exit are allowed to have too)
        enemy = None
        if random.choice([True, False]):
            enemy = random.choice(enemies)
            # create a fresh copy with same stats
            enemy = Enemy(name=enemy.name, life=enemy.max_life, weapon=enemy.weapon, armor=enemy.armor, description=enemy.description)
        room = Room(idx=i, description=random.choice(room_texts["rooms"]), enemy=enemy)
        rooms.append(room)
    dungeon = Dungeon(rooms=rooms)
    return dungeon, room_texts

def main():
    dungeon, room_texts = create_dungeon()
    player = create_player()
    print(f"Вы — {player.name}. {player.description} \nВаше снаряжение - {player.weapon.description}, {player.armor.description}")
    controller = GameController(dungeon=dungeon, player=player, room_texts=room_texts, input_provider=InputProvider())
    controller.run()

main()
