"""This runs the game application."""

import os

from game import GameApp

# default language = English
# Use "ko" for Korean and "ja" for Japanese
LANG = "en"
# default GameAI = "gemini"
AI_TARGET = "gemini"

DEBUG = False
if "GAME_LANG" in os.environ:
    LANG = os.environ.get("GAME_LANG")
if "GAME_DEBUG" in os.environ:
    DEBUG = bool(os.environ.get("GAME_DEBUG"))
if "GAME_AI" in os.environ:
    AI_TARGET = os.environ.get("GAME_AI")

match AI_TARGET:
    case "gemma":
        from gemma import GameAI

    case "gemma_ollama":
        from gemma_ollama import GameAI

    case "gemini":
        from gemini import GameAI

    case _:
        from scripted import GameAI

trail = GameApp()
game_ai = GameAI(trail)

# Main game loop
trail.initialize_game(game_ai, LANG, DEBUG)
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
