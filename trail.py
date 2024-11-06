import random

from game import GameApp

trail = GameApp()

# Main game loop
trail.initialize_game()
while True:
    trail.display_status()
    choice = trail.get_player_choice()
    if choice == 1:
        trail.travel()
        if random.random() < 1:  # 30% chance of a random event after traveling
            trail.random_event()
        if trail.remove_dead_members():  # Remove dead members after traveling
            break
    elif choice == 2:
        trail.rest()
    elif choice == 3:
        trail.search()
    elif choice == 4:
        pass  # Already displayed status at the beginning of the loop
    elif choice == 5:
        print("Quitting the game.")
        break
    if trail.check_game_over():
        break
