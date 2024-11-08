"""This runs the game application."""

import os
import random

from game import GameApp
#from scripted import GameAI
#from gemma import GameAI
#from gemma_ollama import GameAI
from gemini import GameAI

# default language = English
# Use "ko" for Korean and "ja" for Japanese
lang = "en"
debug = False
if "GAME_LANG" in os.environ:
    lang = os.environ.get("GAME_LANG")
if "GAME_DEBUG" in os.environ:
    debug = bool(os.environ.get("GAME_DEBUG"))

trail = GameApp()
game_ai = GameAI(trail)

# Main game loop
trail.initialize_game(game_ai, lang, debug)
while True:
    trail.display_status()
    choice = trail.get_player_choice()
    if choice == 1:
        trail.travel()
        trail.random_event()
    elif choice == 2:
        trail.rest()
    elif choice == 3:
        trail.search()
    elif choice == 4:
        pass  # Already displayed status at the beginning of the loop
    elif choice == 5:
        trail.quit()
        break

    trail.remove_dead_members()  # Remove dead members after traveling
    if trail.check_game_over():
        break
