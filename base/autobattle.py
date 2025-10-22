from .models import Player, Enemy

def autobattle(player: Player, enemy: Enemy, output_func=print):
    # Returns True if player won, False if player died
    output_func(f"Бой начался: {player.name} vs {enemy.name}")
    turn = 0
    while player.is_alive and enemy.is_alive:
        turn += 1
        # player attacks
        if player.attack_hit():
            dmg = player.compute_damage()
            enemy.receive_damage(dmg)
            output_func(f"[{turn}] {player.name} попал и нанес {dmg} урона. (Жизни врага: {enemy.life}/{enemy.max_life})")
        else:
            output_func(f"[{turn}] {player.name} промахнулся.")
        if not enemy.is_alive:
            output_func(f"{enemy.name} повержен.")
            break
        # enemy attacks
        if enemy.attack_hit():
            dmg = enemy.compute_damage()
            player.receive_damage(dmg)
            output_func(f"[{turn}] {enemy.name} попал и нанес {dmg} урона. (Жизни игрока: {player.life}/{player.max_life})")
        else:
            output_func(f"[{turn}] {enemy.name} промахнулся.")
        if not player.is_alive:
            output_func("Игрок повержен.")
            break
    return player.is_alive
