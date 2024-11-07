import random

from game import GameApp
#from scripted import GameAI
#from gemma import GameAI
#from gemma_ollama import GameAI
from gemini import GameAI

trail = GameApp()
game_ai = GameAI(trail)

# Main game loop
trail.initialize_game(game_ai)
while True:
    trail.display_status()
    choice = trail.get_player_choice()
    if choice == 1:
        trail.travel()
        if random.random() < 0.3:  # 30% chance of a random event after traveling
            trail.random_event()
    elif choice == 2:
        trail.rest()
    elif choice == 3:
        trail.search()
    elif choice == 4:
        pass  # Already displayed status at the beginning of the loop
    elif choice == 5:
        print("Quitting the game.")
        break

    if trail.remove_dead_members():  # Remove dead members after traveling
        break

    if trail.check_game_over():
        break
