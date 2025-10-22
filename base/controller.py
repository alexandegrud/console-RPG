from .models import Dungeon, Room, Player
from .autobattle import autobattle

class InputProvider:
    def __init__(self, prompt_func=input):
        self.prompt_func = prompt_func

    def get(self, prompt: str):
        return self.prompt_func(prompt)

class GameController:
    def __init__(self, dungeon: Dungeon, player: Player, room_texts: dict, input_provider: InputProvider = None, output_func=print):
        self.dungeon = dungeon
        self.player = player
        self.room_texts = room_texts
        self.pos = dungeon.start_index
        self.input_provider = input_provider or InputProvider()
        self.output = output_func
        self.action_results = room_texts.get("action_results", [])

    def describe_room(self, room: Room):
        room_desc = room.description
        self.output(f"Комната {room.idx + 1}: {room_desc}")
        if room.enemy and room.enemy.is_alive:
            self.output(f"В комнате есть враг: {room.enemy.name} - {room.enemy.description}"
                        f"Снаряжение врага: Оружие - {room.enemy.weapon.name}, Доспехи - {room.enemy.armor.name}.")
        else:
            self.output("Комната пуста.")

    def available_actions(self, room: Room):
        actions = []
        if room.enemy and room.enemy.is_alive:
            actions.append(("Атаковать", self.action_attack))
        else:
            if room.idx != self.dungeon.exit_index:
                actions.append(("Пойти дальше", self.action_forward))
            if room.idx != 0:
                actions.append(("Вернуться назад", self.action_back))
            if room.idx == self.dungeon.exit_index:
                actions.append(("Выйти из подземелья", self.action_exit))
        return actions

    def action_attack(self, room: Room):
        # If autobattle module exists, perform autobattle
        if room.enemy and room.enemy.is_alive:
            won = autobattle(self.player, room.enemy, output_func=self.output)
            if won:
                self.output("Вы победили")
            else:
                self.output("Вы были побеждены в бою.")
        return None

    def action_forward(self, room: Room):
        if self.pos < len(self.dungeon.rooms)-1:
            self.pos += 1
        return None

    def action_back(self, room: Room):
        if self.pos > 0:
            self.pos -= 1
        return None

    def action_exit(self, room: Room):
        self.output("Вы вышли из подземелья. Игра завершена.")
        return "exit"

    def run(self):
        running = True
        while running:
            room = self.dungeon.rooms[self.pos]
            self.describe_room(room)
            actions = self.available_actions(room)
            # show actions
            for i, (name, _) in enumerate(actions, start=1):
                self.output(f"{i}. {name}")
            # get choice
            choice_raw = self.input_provider.get("Выберите действие (номер): ")
            try:
                choice = int(choice_raw.strip())
            except Exception:
                self.output("Неверный ввод. Попробуйте снова.")
                continue
            if not (1 <= choice <= len(actions)):
                self.output("Неверный номер действия.")
                continue
            action = actions[choice-1][1]
            result = action(room)
            if result == "exit":
                running = False
            if not self.player.is_alive:
                self.output("Вы погибли. Игра окончена.")
                running = False

